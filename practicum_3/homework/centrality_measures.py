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
    n = G.number_of_nodes()

    for node in G.nodes():
        distances = nx.single_source_shortest_path_length(G, node)

        total_distance = sum(distances.values())

        if total_distance > 0:
            centrality[node] = (n - 1) / total_distance
        else:
            centrality[node] = 0.0

    return centrality


def betweenness_centrality(G: AnyNxGraph) -> dict[Any, float]:
    dict_res = {i: 0.0 for i in G.nodes()}

    for i,j in combinations(G.nodes(), 2):
        paths = list(nx.all_shortest_paths(G, i, j))
        path_len = len(paths)
        if path_len > 0:
            for path in paths:
                for node in path:
                    dict_res[node] += path_len

    return dict_res


def eigenvector_centrality(G: AnyNxGraph) -> dict[Any, float]: 
    ln = len(G)

    if ln < 0:
        return {}

    vec_one = np.ones(ln) / np.linalg.norm(np.ones(ln))

    matrix_adjency = nx.adjacency_matrix(G).toarray()

    for i in range(101):
        vec_one_copy = vec_one.copy()
        vec_one = matrix_adjency @ vec_one
        vec_one = vec_one / np.linalg.norm(vec_one)
        if np.linalg.norm(vec_one) == 0:
            return {x: 0.0 for x in G.nodes()}
        if (np.linalg.norm(vec_one_copy) - np.linalg.norm(vec_one)) < 1e-6:
            return {x: vec_one[j] for j, x in enumerate(G.nodes())}
    raise Exception

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

