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

    for node in nodes:
        try:
            total_distance = sum(nx.shortest_path_length(G, source=node).values())
            if total_distance > 0:
                centrality[node] = (n - 1) / total_distance
            else:
                centrality[node] = 0.0
        except nx.NetworkXError:
            centrality[node] = 0.0

    return centrality


def betweenness_centrality(G: AnyNxGraph) -> dict[Any, float]:
    centrality = {node: 0.0 for node in G.nodes()}
    nodes = list(G.nodes())

    for s, t in combinations(nodes, 2):
        if s == t:
            continue
        try:
            paths = list(nx.all_shortest_paths(G, source=s, target=t))
            if paths:
                summ = len(paths)
                for path in paths:
                    for node in path[1:-1]:
                        centrality[node] += 1.0 / summ
        except nx.NetworkXNoPath:
            continue

    n = len(nodes)
    if n > 2:
        scale = 2.0 / ((n - 1) * (n - 2))
        centrality = {k: v * scale for k, v in centrality.items()}

    return centrality


def eigenvector_centrality(G: AnyNxGraph) -> dict[Any, float]:
    nodes = list(G.nodes())
    n = len(nodes)
    A = nx.adjacency_matrix(G, nodelist=nodes).todense().astype(float)

    eigenvalues, eigenvectors = np.linalg.eig(A)
    max_idx = np.argmax(eigenvalues)
    principal_eigenvector = eigenvectors[:, max_idx].real

    centrality = {nodes[i]: float(principal_eigenvector[i]) for i in range(n)}

    min_val = min(centrality.values())
    if min_val < 0:
        centrality = {k: v - min_val for k, v in centrality.items()}

    max_val = max(centrality.values())
    if max_val > 0:
        centrality = {k: v / max_val for k, v in centrality.items()}

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