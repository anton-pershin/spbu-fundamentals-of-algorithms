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
    nodes = G.nodes()
    for node in nodes:
        total_distance = 0
        shortest_paths = nx.single_source_shortest_path_length(G, node)
        total_distance = sum(shortest_paths.values())
        centrality[node] = 1 / total_distance if total_distance != 0 else 0
    return centrality


def betweenness_centrality(G: AnyNxGraph) -> dict[Any, float]: 
    nodes = G.nodes()
    centrality = {node: 0.0 for node in nodes}
    
    for s in nodes:
        S = []
        P = {v: [] for v in nodes}
        sigma = {v: 0 for v in nodes}
        sigma[s] = 1
        d = {v: -1 for v in nodes}
        d[s] = 0
        Q = [s]
        
        while Q:
            v = Q.pop(0)
            S.append(v)
            for w in G.neighbors(v):
                if d[w] < 0:
                    Q.append(w)
                    d[w] = d[v] + 1
                if d[w] == d[v] + 1:
                    sigma[w] += sigma[v]
                    P[w].append(v)
        
        delta = {v: 0 for v in nodes}
        while S:
            w = S.pop()
            for v in P[w]:
                delta[v] += (sigma[v] / sigma[w]) * (1 + delta[w])
            if w != s:
                centrality[w] += delta[w]
    
    if not nx.is_directed(G):
        n = len(nodes)
        scale = 1 / ((n - 1) * (n - 2)) if n > 2 else 1
        centrality = {k: v * scale for k, v in centrality.items()}
    
    return centrality


def eigenvector_centrality(G: AnyNxGraph, max_iter=100, tol=1.0e-6) -> dict[Any, float]:
    A = nx.adjacency_matrix(G).astype(float)
    n = A.shape[0]
    x = np.ones(n) / n
    
    for _ in range(max_iter):
        x_new = A @ x
        x_new /= np.linalg.norm(x_new, 2)
        if np.linalg.norm(x_new - x, 2) < tol:
            break
        x = x_new
    
    centrality = {node: x[i] for i, node in enumerate(G.nodes())}
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

