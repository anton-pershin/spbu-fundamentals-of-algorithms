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
    n = len(G)
    for v in G:
        path = nx.shortest_path_length(G, v)
        dist = sum(path.values())

        if dist > 0:
            res[v] = (n - 1) * (1 / dist)
        else:
            res[v] = 0

    return res


def betweenness_centrality(G: AnyNxGraph) -> dict[Any, float]: 
    res = {}
    for v in G:
        res[v] = 0.0
    num = len(G)
    
    for s in G:
        for t in G:
            if s != t:
                all_paths = list(nx.all_shortest_paths(G, s, t))
                n = len(all_paths)
                for path in all_paths:
                    for v in path[1: -1]:
                        res[v] += 1 / n

    norm = (num - 1) * (num - 2)
    for x in res:
        res[x] /= norm
    return res


def eigenvector_centrality(G: AnyNxGraph) -> dict[Any, float]: 
    c = {}
    for v in G:
        c[v] = 1.0

    A = nx.to_numpy_array(G)
    eigenvalues = np.linalg.eigvals(A)
    l = max(abs(eigenvalues))

    for i in range(100):
        c1 = {}
        for v in G:
            if G.is_directed():
                s = sum(c[u] for u in G.predecessors(v))
            else:
                s = sum(c[u] for u in G.neighbors(v))

            c1[v] = (1 / l) * s
        norm = sum(x**2 for x in c1.values())**0.5
        for v in c1:
            c1[v] = c1[v] / norm
        c = c1
    return c


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