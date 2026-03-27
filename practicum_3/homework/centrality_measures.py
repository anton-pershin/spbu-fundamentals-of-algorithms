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
    n = len(G)

    for v in G.nodes:
        lengths = nx.single_source_shortest_path_length(G, v)
        total_dist = sum(lengths.values())

        if total_dist > 0 and n > 1:
            centrality[v] = (n - 1) / total_dist
        else:
            centrality[v] = 0.0

    return centrality

def betweenness_centrality(G: AnyNxGraph) -> dict[Any, float]: 
    centrality = dict.fromkeys(G.nodes, 0.0)

    nodes = list(G.nodes)

    for s, t in combinations(nodes, 2):
        paths = list(nx.all_shortest_paths(G, s, t))
        num_paths = len(paths)

        for path in paths:
            for v in path[1:-1]: 
                centrality[v] += 1 / num_paths

    n = len(G)
    if n > 2:
        scale = 1 / ((n - 1) * (n - 2) / 2)
        for v in centrality:
            centrality[v] *= scale

    return centrality


def eigenvector_centrality(G: AnyNxGraph) -> dict[Any, float]: 
    A = nx.to_numpy_array(G)
    
    eigenvalues, eigenvectors = np.linalg.eig(A)

    max_index = np.argmax(eigenvalues.real)
    vec = eigenvectors[:, max_index].real
    vec = np.abs(vec)
    vec = vec / np.linalg.norm(vec)

    return {node: float(vec[i]) for i, node in enumerate(G.nodes)}

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

    print(nx.closeness_centrality(G))
    print(closeness_centrality(G))





