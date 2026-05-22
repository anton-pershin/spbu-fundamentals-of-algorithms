from typing import Any, Protocol
from itertools import combinations

import numpy as np
import networkx as nx

from src.plotting.graphs import plot_graph, plot_network_via_plotly
from src.common import AnyNxGraph 


class CentralityMeasure(Protocol):
    def __call__(self, G: AnyNxGraph) -> dict[Any, float]:
        ...


def closeness_centrality(G: AnyNxGraph) -> dict[Any, float]:
    centrality = {}
    
    nodes = list(G.nodes())
    n = len(nodes)
    
    for v in nodes:
        distances = nx.single_source_shortest_path_length(G, v)
        total_distance = sum(distances.values())
        
        if total_distance > 0:
            centrality[v] = (n - 1) / total_distance
        else:
            centrality[v] = 0.0
    
    return centrality


def betweenness_centrality(G: AnyNxGraph) -> dict[Any, float]:
    nodes = list(G.nodes())
    n = len(nodes)
    centrality = {v: 0.0 for v in nodes}
    
    for s in nodes:
        stack = []
        pred = {v: [] for v in nodes}
        distance = {v: -1 for v in nodes}
        cnt_short_way = {v: 0 for v in nodes}
        
        distance[s] = 0
        cnt_short_way[s] = 1
        queue = [s]
        
        while queue:
            v = queue.pop(0)
            stack.append(v)
            for w in G.neighbors(v):
                if distance[w] < 0:
                    queue.append(w)
                    distance[w] = distance[v] + 1
                if distance[w] == distance[v] + 1:
                    cnt_short_way[w] += cnt_short_way[v]
                    pred[w].append(v)
        
        delta = {v: 0.0 for v in nodes}
        while stack:
            w = stack.pop()
            for v in pred[w]:
                delta[v] += (cnt_short_way[v] / cnt_short_way[w]) * (1 + delta[w])
            if w != s:
                centrality[w] += delta[w]
    
    if n > 2:
        for v in nodes:
            centrality[v] /= ((n - 1) * (n - 2))
    
    return centrality


def eigenvector_centrality(G: AnyNxGraph) -> dict[Any, float]:
    nodes = list(G.nodes())
    n = len(nodes)
    
    A = nx.adjacency_matrix(G).todense()
    A = np.array(A, dtype=float)
    x = np.ones(n)
    
    max_iter = 1000
    differ = 1e-8
    
    for i in range(max_iter):
        x_new = A @ x 
        norm = np.linalg.norm(x_new, ord=np.inf)
        if norm > 0:
            x_new = x_new / norm
        
        if np.linalg.norm(x_new - x, ord=np.inf) < differ:
            break
        x = x_new
    
    centrality = {}
    for i, node in enumerate(nodes):
        centrality[node] = float(x[i])
    
    return centrality

def plot_centrality_measure(G: AnyNxGraph, measure: CentralityMeasure) -> None:
    values = measure(G)
    if values is not None:
        plot_graph(G, node_weights=values, figsize=(14, 8), name=measure.__name__)
    else:
        print(f"Implement {measure.__name__}")


if __name__ == "__main__":
    G = nx.karate_club_graph()
    
    plot_centrality_measure(G, closeness_centrality)
    plot_centrality_measure(G, betweenness_centrality)
    plot_centrality_measure(G, eigenvector_centrality)

