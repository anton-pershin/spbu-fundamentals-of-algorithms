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
    cls_centrality = dict()
    for node in G.nodes():
        distances = nx.single_source_shortest_path_length(G, node)
        total_distance = sum(distances.values())
        if total_distance > 0:
            cls_centrality[node] = (len(distances) - 1) / total_distance
        else:
            cls_centrality[node] = 0.0
    return cls_centrality


def betweenness_centrality(G: AnyNxGraph) -> dict[Any, float]: 
    btwns_centrality = dict()
    for node in G.nodes():
        btwns_centrality[node] = 0.0
        for start, end in combinations(G.nodes(), 2):
            if start == node or end == node:
                continue
            paths = list(nx.all_shortest_paths(G, start, end))
            for path in paths:
                if node in path:
                    btwns_centrality[node] += 1 / len(paths)
    for node in G.nodes():
        btwns_centrality[node] /= (len(G.nodes()) - 1) * (len(G.nodes()) - 2) / 2
    return btwns_centrality 


def eigenvector_centrality(G: AnyNxGraph) -> dict[Any, float]:
    eigen_centrality = {}
    nodes = list(G.nodes())
    eigenvalues, eigenvectors = np.linalg.eigh(nx.adjacency_matrix(G).todense())
    major_eigenvector = eigenvectors[:, np.argmax(eigenvalues)]
    for i in range(len(nodes)):
        eigen_centrality[nodes[i]] = float(major_eigenvector[i])
    return eigen_centrality

def plot_centrality_measure(G: AnyNxGraph, measure: CentralityMeasure) -> None:
    values = measure(G)
    if values is not None:
        plot_graph(G, node_weights=values, figsize=(14, 8), name=measure.__name__)
    else:
        print(f"Implement {measure.__name__}")

def equalty_check(comment: str, epsilon: int, result1: dict[Any, float], result2: dict[Any, float]) -> bool:
    print(comment)
    if all(abs(result1[node] - result2[node]) < epsilon for node in result1.keys()):
        print("Results are equal")
        return True
    else:
        print("Results are not equal")
        return False

if __name__ == "__main__":
    G = nx.karate_club_graph()
    
    # plot_centrality_measure(G, closeness_centrality)
    # plot_centrality_measure(G, betweenness_centrality)
    # plot_centrality_measure(G, eigenvector_centrality)

    equalty_check("Closeness centrality check: ", 0.0001, closeness_centrality(G), nx.closeness_centrality(G))
    equalty_check("Betweenness centrality check: ", 0.0001, betweenness_centrality(G), nx.betweenness_centrality(G))
    equalty_check("Eigenvector centrality check: ", 0.1, eigenvector_centrality(G), nx.eigenvector_centrality(G))