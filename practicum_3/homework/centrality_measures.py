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
    res = {}

    for node in G.nodes():
        dist = nx.single_source_shortest_path_length(G, node)
        distance = sum(dist.values())
        n = len(dist)

        if distance == 0:
            res[node] = 0.0
        else:
            res[node] = (n - 1) / distance

    return res


def betweenness_centrality(G: AnyNxGraph) -> dict[Any, float]:
    result = {node: 0.0 for node in G.nodes()}
    for i, j in combinations(G.nodes(), 2):
        paths = list(nx.all_shortest_paths(G, i, j))
        if len(paths) > 0:
            for path in paths:
                for node in path[1:-1]:
                    result[node] += 1.0 / len(paths)
    n = G.number_of_nodes()
    normalization = (n - 1) * (n - 2) / 2
    for node in result:
        result[node] /= normalization
    return result

    pass


def eigenvector_centrality(G: AnyNxGraph) -> dict[Any, float]:
    nodes = list(G.nodes())
    n = len(nodes)
    A = nx.adjacency_matrix(G).toarray()
    c = np.ones(n)

    for i in range(100):
        c = A @ c
        c = c / np.linalg.norm(c)

    res = {nodes[i]: c[i] for i in range(n)}
    return res

    pass


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

