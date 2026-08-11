from typing import Any, Protocol
from itertools import combinations

import numpy as np
import networkx as nx

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph

class CentralityMeasure(Protocol):
    def __call__(self, G: AnyNxGraph) -> dict[Any, float]:
        ...

def closeness_centrality(G: AnyNxGraph) -> dict[Any, float]:
    n = G.number_of_nodes()

    centrality = {}
    
    for node in G.nodes():
        distances = nx.single_source_shortest_path_length(G, node)

        total_distance = sum(distances.values())

        if total_distance > 0:
            c_v = 1.0 / total_distance
            centrality[node] = c_v / n
        else:
            centrality[node] = 0.0

    return centrality


def betweenness_centrality(G: AnyNxGraph) -> dict[Any, float]:
    nodes = list(G.nodes())
    n = len(nodes)
    centrality = {node: 0.0 for node in nodes}

    for i in range(n):
        for j in range(i + 1, n):
            s, t = nodes[i], nodes[j]

            try:
                all_paths = list(nx.all_shortest_paths(G, source=s, target=t))
            except nx.NetworkXNoPath:
                continue

            total_paths = len(all_paths)
            if total_paths == 0:
                continue

            for path in all_paths:
                for v in path[1:-1]:  
                    centrality[v] += 1.0 / total_paths

    return centrality

def eigenvector_centrality(G: AnyNxGraph) -> dict[Any, float]:
    A = nx.to_numpy_array(G)
    n = A.shape[0]

    if n == 0:
        return {}

    eigenvalues, eigenvectors = np.linalg.eig(A)
    max_eigenvalue_idx = np.argmax(np.abs(eigenvalues))
    
    eigenvector = np.real(eigenvectors[:, max_eigenvalue_idx])
    eigenvector = np.abs(eigenvector)
    centrality = {node: eigenvector[i] for i, node in enumerate(G.nodes())}
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
