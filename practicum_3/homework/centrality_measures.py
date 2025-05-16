from typing import Any, Protocol
from itertools import combinations
from collections import deque
import numpy as np
import networkx as nx

from src.plotting.graphs import plot_graph, plot_network_via_plotly
from src.common import AnyNxGraph 

class CentralityMeasure(Protocol):
    def __call__(self, G: AnyNxGraph) -> dict[Any, float]:
        ...


def closeness_centrality(G: AnyNxGraph) -> dict[Any, float]:
    centrality = {}
    nodes = G.nodes()

    for node in nodes:
        paths = nx.single_source_shortest_path_length(G, node).values()
        total_dist = sum(paths)
        node_cl_cent = (len(nodes) - 1) / total_dist if total_dist > 0 else 0

        centrality[node] = node_cl_cent
        
    return centrality



def betweenness_centrality(G: AnyNxGraph) -> dict[Any, float]:
    centrality = {}
    nodes = G.nodes()
    for node in nodes:
        centrality[node] = 0

    for v in nodes:
        stack = []
        sigma = {n: 0 for n in nodes}
        pred = {n: [] for n in nodes}
        sigma[v] = 1
        dist = {n: -1 for n in nodes}
        dist[v] = 0
        queue = deque([v])
        
        while len(queue) > 0:
            s = queue.popleft()
            stack.append(s)
            for n_neigh in G.neighbors(s):
                if dist[n_neigh] < 0:
                    queue.append(n_neigh)
                    dist[n_neigh] = dist[s] + 1
                if dist[n_neigh] == dist[s] + 1:
                    sigma[n_neigh] += sigma[s]
                    pred[n_neigh].append(s)
        
        delta = {n: 0 for n in nodes}
        while len(stack) > 0:
            b = stack.pop()
            for u in pred[b]:
                delta[u] += (sigma[u] / sigma[b]) * (1 + delta[b])
            if b != v:
                centrality[b] += delta[b]
    
    for node in nodes:
        centrality[node] /= 2
    
    return centrality


def eigenvector_centrality(G: AnyNxGraph, iterations=100, diff=1.0e-6) -> dict[Any, float]:
    centrality = {}
    nodes = G.nodes()
    A = nx.adjacency_matrix(G).astype(float)
    x = np.ones(len(nodes))
    
    for _ in range(iterations):
        x_new = A @ x
        x_new /= np.linalg.norm(x_new, 2)
        if np.linalg.norm(x_new - x, 2) < diff:
            x = x.tolist()
            break
        x = x_new
    
    for index, node in enumerate(nodes):
        centrality[node] = x[index]
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