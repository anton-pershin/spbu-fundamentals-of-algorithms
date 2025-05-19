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
    n = len(G)
    centrality: dict[Any, float] = {}
    for v in G:
        lengths = nx.single_source_shortest_path_length(G, v)
        total = sum(lengths.values())
        if total > 0.0 and n > 1:
            centrality[v] = (len(lengths) - 1) / total
        else:
            centrality[v] = 0.0
    return centrality


def betweenness_centrality(G: AnyNxGraph) -> dict[Any, float]:
    nodes = list(G)
    betweenness = dict.fromkeys(nodes, 0.0)

    for u, v in combinations(nodes, 2):
        try:
            paths = list(nx.all_shortest_paths(G, source=u, target=v))
        except nx.NetworkXNoPath:
            continue

        count = len(paths)
        for path in paths:
            for w in path[1:-1]:
                betweenness[w] += 1.0 / count
    
    if len(G) > 2:
        scale = 1.0 / ((len(G) - 1) * (len(G) - 2)) if G.is_directed() else 2.0 / ((len(G) - 1) * (len(G) - 2))
        for v in betweenness:
            betweenness[v] *= scale
    return betweenness


def eigenvector_centrality(G: AnyNxGraph, max_iter: int = 1000, tol: float = 1.0e-6) -> dict[Any, float]:
    nodelist = list(G)
    A = nx.to_numpy_array(G, nodelist=nodelist)
    n = A.shape[0]
    x = np.ones(n)
    for _ in range(max_iter):
        x_last = x.copy()
        x = A.dot(x)
        norm = np.linalg.norm(x)
        if norm == 0:
            return dict.fromkeys(nodelist, 0.0)
        x /= norm
        if np.linalg.norm(x - x_last) < tol:
            break
    centrality = {node: float(x[i]) for i, node in enumerate(nodelist)}
    return centrality


def plot_centrality_measure(G: AnyNxGraph, measure: CentralityMeasure) -> None:
    values = measure(G)
    if values is not None:
        plot_graph(G, node_weights=values, figsize=(14, 8), name=measure.__name__)
    else:
        print(f"Implement {measure.__name__}")


if __name__ == "__main__":
    G = nx.karate_club_graph()

    cc = closeness_centrality(G)
    bc = betweenness_centrality(G)
    ec = eigenvector_centrality(G)

    nx_cc = nx.closeness_centrality(G)
    nx_bc = nx.betweenness_centrality(G)
    nx_ec = nx.eigenvector_centrality(G, max_iter=1000, tol=1.0e-6)

    tol = 1e-6
    assert all(abs(cc[n] - nx_cc[n]) < tol for n in G), "Closeness centrality does not match networkx"
    assert all(abs(bc[n] - nx_bc[n]) < tol for n in G), "Betweenness centrality does not match networkx"
    assert all(abs(ec[n] - nx_ec[n]) < 1e-1 for n in G), "Eigenvector centrality does not match networkx"

    plot_centrality_measure(G, closeness_centrality)
    plot_centrality_measure(G, betweenness_centrality)
    plot_centrality_measure(G, eigenvector_centrality)
