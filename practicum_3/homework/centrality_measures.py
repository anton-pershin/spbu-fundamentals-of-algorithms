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

    result = {}
    n = G.number_of_nodes()

    for i in G.nodes():
        distances = nx.shortest_path_length(G, source=i) 

        total_distance = sum(distances.values())
        result[i] = 1.0 / total_distance

    return result


def betweenness_centrality(G: AnyNxGraph) -> dict[Any, float]: 

    result = {v: 0.0 for v in G.nodes()}

    nodes = list(G.nodes())
    n = len(nodes)

    for s in nodes:
        for t in nodes:
            if s == t: 
                continue

            paths = list(nx.all_shortest_paths(G, source=s, target=t))
            total_paths = len(paths)

            for path in paths:
                for v in path[1:-1]:
                    result[v] += 1.0 / total_paths
    
    for v in result:
        result[v] = result[v] / ((n - 1) * (n - 2))

    return result


def eigenvector_centrality(G: AnyNxGraph) -> dict[Any, float]: 

    A = nx.adjacency_matrix(G).toarray()

    eigenvalues, eigenvectors = np.linalg.eig(A)

    max_index = np.argmax(eigenvalues)

    eigenvector = eigenvectors[:, max_index]

    eigenvector = np.abs(eigenvector)

    eigenvector = eigenvector / np.max(eigenvector)

    result = {node: eigenvector[i] for i, node in enumerate(G.nodes())}

    return result


def plot_centrality_measure(G: AnyNxGraph, measure: CentralityMeasure) -> None:
    values = measure(G)
    if values is not None:
        plot_graph(G, node_weights=values, figsize=(14, 8), name=measure.__name__)
    else:
        print(f"Implement {measure.__name__}")


# if __name__ == "__main__":
#     G = nx.karate_club_graph()
    
#     plot_centrality_measure(G, closeness_centrality)
#     plot_centrality_measure(G, betweenness_centrality)
#     plot_centrality_measure(G, eigenvector_centrality)

if __name__ == "__main__":
    G = nx.karate_club_graph()
    
    print("Closeness Centrality:")
    print(closeness_centrality(G))
    print("\nBetweenness Centrality:")
    print(betweenness_centrality(G))
    print("\nEigenvector Centrality:")
    print(eigenvector_centrality(G))