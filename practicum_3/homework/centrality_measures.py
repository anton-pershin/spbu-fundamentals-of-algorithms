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

    n = len(G)
    centrality = {}
    
    for node in G.nodes():
        lengths = nx.single_source_shortest_path_length(G, node)
        total_dist = sum(lengths.values())
        centrality[node] = 1.0 / total_dist * n
    
    return centrality
            


def betweenness_centrality(G: AnyNxGraph) -> dict[Any, float]: 

    centrality = {node : 0.0 for node in G.nodes()}
    nodes = list(G.nodes())

    for s, t in combinations(nodes, 2):
        paths = list(nx.all_shortest_paths(G, s, t))
        num_paths = len(paths)
        for path in paths:
            for v in path[1:-1]:
                centrality[v] += 1.0 / num_paths

    return centrality


def eigenvector_centrality(G: AnyNxGraph) -> dict[Any, float]: 

    nodes = list(G.nodes())
    n = len(nodes)

    A = nx.adjacency_matrix(G, nodelist=nodes).toarray()
    x = np.ones(n)

    for i in range(n):
        xn = np.zeros(n)
        for u in range(n):
            for v in range(n):
                if A[u, v] == 1:
                    xn[u] += x[v]
        
        norm = np.linalg.norm(xn)

        x = xn / norm

    return {nodes[i]: x[i] for i in range(n)}


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

