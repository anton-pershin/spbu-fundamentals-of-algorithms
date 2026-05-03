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
    nodes = {}
    n = len(G) - 1

    for node in G:
        sum_dist = sum(nx.single_source_bellman_ford_path_length(G, node).values())
        if sum_dist == 0:
            nodes[node] = 0.0
        else:
            nodes[node] = n/sum_dist

    return nodes


def betweenness_centrality(G: AnyNxGraph) -> dict[Any, float]: 
    n = len(G)
    nodes = {node: 0.0 for node in G.nodes()}
    
    all_pairs = combinations(G.nodes(), 2)

    for s, t in all_pairs:
        paths_between = list(nx.all_shortest_paths(G, source=s, target=t))
        paths_count = len(paths_between)
        for path in paths_between:
            for i in path[1:-1]:
                nodes[i] += 1/paths_count

    return nodes


def eigenvector_centrality(G: AnyNxGraph) -> dict[Any, float]: 

    n = len(G)
    nodes = list(G.nodes())
    A = nx.adjacency_matrix(G, nodelist=nodes).toarray()

    x = np.ones(n)
    x = x / np.linalg.norm(x) 

    for i in range(100):
        x_copy = x.copy()
        x = A @ x
        norming_x = np.linalg.norm(x)
        if norming_x == 0:
            return {node: 0.0 for node in nodes}
        x = x/norming_x
        if np.linalg.norm(x-x_copy) < 1e-6:
            return {node: x[j] for j, node in enumerate(nodes)}
    else:
        raise nx.exception.NetworkXNotConverged()


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

