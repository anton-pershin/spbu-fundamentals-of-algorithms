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
    n = len(G) - 1
    result = dict()
    for current_node in G.nodes():
        s = sum(nx.single_source_bellman_ford_path_length(G, current_node).values()) 
        if s != 0:
            result[current_node] = n / s
        else:
            result[current_node] = 0.0
    return result

def betweenness_centrality(G: AnyNxGraph) -> dict[Any, float]: 

    result = {node: 0.0 for node in G.nodes()}

    for s, t in combinations(G.nodes(), 2):
        paths = tuple(nx.all_shortest_paths(G, source=s, target=t))
        path_count = len(paths)
        for path in paths:
            for node_on_way in path[1:-1]:
                result[node_on_way] += (1 / path_count)

    n = len(G)
    if n > 2:
        for i in G.nodes():
            result[i] = result[i] / ( (n-1)*(n-2) / 2)
    return result



def eigenvector_centrality(G: AnyNxGraph) -> dict[Any, float]:
    n = len(G)
    if n == 0:
        return {}
    x = np.ones(n) / np.linalg.norm(np.ones(n))
    nodes = list(G.nodes())
    A = nx.adjacency_matrix(G, nodelist=nodes).toarray()

    for i in range(100):
        x_copy = x.copy()
        x = A @ x
        norm = np.linalg.norm(x)
        if norm == 0:
            return {node: 0.0 for node in nodes}
        x = x / norm
        if (np.linalg.norm(x - x_copy) < 1e-6):
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

