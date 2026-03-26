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
    data = {}
    for node in G:
        length = nx.shortest_path_length(G, source = node)
        dist = sum(length.values())
        if dist > 0:
            data[node] = (n-1) / dist
        else:
            data[node] = 0

    return data

def betweenness_centrality(G: AnyNxGraph) -> dict[Any, float]: 
    n = G.number_of_nodes()
    data = {}
    for node in G:
        betweenness = 0
        for source, target in combinations(G.nodes(), 2):
            if node == source or node == target or target == source:
                continue

            paths = list(nx.all_shortest_paths(G, source = source, target = target))
            total = len(paths)
            if total == 0:
                continue

            trough_node = sum([1 for path in paths if node in path and path.index(node) not in (0, len(path) - 1)])
            betweenness += trough_node / total

        betweenness_norm = ((n-1)*(n-2))/2
        data[node] = betweenness / betweenness_norm
    
    return data


def eigenvector_centrality(G: AnyNxGraph) -> dict[Any, float]: 
    ...


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

