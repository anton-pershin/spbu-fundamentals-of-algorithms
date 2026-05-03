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
    closeness = {}

    for n in G.nodes():
        sp = nx.single_source_shortest_path_length(G, n) # shortest path
        totsp = sum(sp.values()) # total shortest path

        if totsp > 0 and len(G) > 1:
            closeness[n] = (len(sp) - 1) / totsp
        else:
            closeness[n] = 0.0

    return closeness


def betweenness_centrality(G):
    betweenness = {n: 0.0 for n in G.nodes()}

    for s, t in combinations(G.nodes(), 2): # source, target
        ps = list(nx.all_shortest_paths(G, s, t)) # paths
        num_ps = len(ps)

        for p in ps: # path in paths
            for n in p[1:-1]: # node
                betweenness[n] += 1 / num_ps

    sc = 1 / ((len(G) - 1) * (len(G) - 2)) # scale - коэфициент нормализации
    for v in betweenness:
        betweenness[v] *= sc

    return betweenness

def eigenvector_centrality(G: AnyNxGraph) -> dict[Any, float]:
    ns = {v: 1 for v in G} # node start
    ns_sum = sum(ns.values())

    x = {k: v / ns_sum for k, v in ns.items()} # key, value
    nnodes = G.number_of_nodes()

    for _ in range(100): # 100 иттераций
        xlast = x.copy()
        x = {k: 0 for k in G.nodes()}

        for n in G.nodes(): # node
            for nbr in G[n]: # neighbour
                x[nbr] += xlast[n]

        norm = sum(v**2 for v in x.values()) ** 0.5 # нормализация
        if norm == 0:
            return {k: 0.0 for k in G.nodes()}

        x = {k: v / norm for k, v in x.items()}
        if sum(abs(x[n] - xlast[n]) for n in x) < nnodes * 1.0e-6:  # 1.0e-6 - погрешность
            return x

    return x

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
