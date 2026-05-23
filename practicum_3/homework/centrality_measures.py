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
    n_nodes = G.number_of_nodes()

    for node in G.nodes():
        dist = nx.single_source_shortest_path_length(G, node)
        total_dist = sum(dist.values())
        if total_dist > 0 and len(dist) > 1:
            centrality[node] = (1.0 / total_dist) / n_nodes
        else:
            centrality[node] = 0.0

    return centrality
def betweenness_centrality(G: AnyNxGraph) -> dict[Any, float]:
    centrality = {node: 0.0 for node in G.nodes()}
    n_nodes = G.number_of_nodes()

    for s in G.nodes():
        for t in G.nodes():
            if s == t:
                continue
            for v in G.nodes():
                if v == s or v == t:
                    continue

                try:
                    all_shortest_paths = list(nx.all_shortest_paths(G, s, t))
                    total_paths = len(all_shortest_paths)
                    if total_paths == 0:
                        continue
                    paths_through_v = 0
                    for path in all_shortest_paths:
                        if v in path[1:-1]:
                            paths_through_v += 1
                    centrality[v] += paths_through_v / total_paths

                except nx.NetworkXNoPath:
                    continue
    return centrality
def eigenvector_centrality(G: AnyNxGraph) -> dict[Any, float]:
    adj_matrix = nx.adjacency_matrix(G).astype(float)
    eigenvalues, eigenvectors = np.linalg.eig(adj_matrix.toarray())
    max_eigenvalue_index = np.argmax(np.abs(eigenvalues))
    eigenvector = eigenvectors[:, max_eigenvalue_index]
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

