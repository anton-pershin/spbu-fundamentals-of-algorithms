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
    n = G.number_of_nodes()
    centrality = {}
    for v in G.nodes():
        lengths = nx.single_source_shortest_path_length(G, v)
        total_dist = sum(lengths.values())
        reachable = len(lengths)
        if total_dist > 0 and n > 1:
            centrality[v] = (reachable - 1) / total_dist * (reachable - 1) / (n - 1)
        else:
            centrality[v] = 0.0
    return centrality


def betweenness_centrality(G: AnyNxGraph) -> dict[Any, float]:
    centrality = dict.fromkeys(G.nodes(), 0.0)
    nodes = list(G.nodes())

    for s, t in combinations(nodes, 2):
        try:
            paths = list(nx.all_shortest_paths(G, s, t))
        except nx.NetworkXNoPath:
            continue

        sigma_st = len(paths)
        contribution = {}
        for path in paths:
            for v in path[1:-1]:
                contribution[v] = contribution.get(v, 0) + 1

        for v, count in contribution.items():
            centrality[v] += count / sigma_st

    n = G.number_of_nodes()
    if n > 2:
        scale = 1 / ((n - 1) * (n - 2) / 2)
        for v in centrality:
            centrality[v] *= scale

    return centrality


def eigenvector_centrality(
    G: AnyNxGraph, max_iter: int = 1000, tol: float = 1e-6
) -> dict[Any, float]:
    nodes = list(G.nodes())
    A = nx.to_numpy_array(G, nodelist=nodes, weight=None)
    n = A.shape[0]

    x = np.ones(n) / n
    for _ in range(max_iter):
        x_new = A @ x
        norm = np.linalg.norm(x_new)
        if norm == 0:
            break
        x_new = x_new / norm
        if np.linalg.norm(x_new - x) < tol:
            x = x_new
            break
        x = x_new

    return dict(zip(nodes, x))


def plot_centrality_measure(G: AnyNxGraph, measure: CentralityMeasure) -> None:
    values = measure(G)
    if values is not None:
        plot_graph(G, node_weights=values, figsize=(14, 8), name=measure.__name__)
    else:
        print(f"Implement {measure.__name__}")

def _verify():
    G = nx.karate_club_graph()
    for name, mine, ref in [
        ("closeness", closeness_centrality(G), nx.closeness_centrality(G)),
        ("betweenness", betweenness_centrality(G), nx.betweenness_centrality(G)),
        ("eigenvector", eigenvector_centrality(G), nx.eigenvector_centrality(G)),
    ]:
        diffs = [abs(mine[v] - ref[v]) for v in G.nodes()]
        print(f"{name}: max diff = {max(diffs):.6f}")

if __name__ == "__main__":
    G = nx.karate_club_graph()

    _verify()

    plot_centrality_measure(G, closeness_centrality)
    plot_centrality_measure(G, betweenness_centrality)
    plot_centrality_measure(G, eigenvector_centrality)
