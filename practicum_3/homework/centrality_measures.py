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
        distances = nx.single_source_shortest_path_length(G, node)
        total = sum(distances.values())
        
        if total == 0:
            centrality[node] = 0.0
        else:
            centrality[node] = (n - 1) / total
        
    return centrality


def betweenness_centrality(G: AnyNxGraph) -> dict[Any, float]: 
    n = len(G) 
    centrality = {node: 0.0 for node in G.nodes()}
    nodes = list(G.nodes())

    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            begin = nodes[i]
            end = nodes[j]

            paths = list(nx.all_shortest_paths(G, begin, end))
            num_paths = len(paths)

            for path in paths:
                for k in range(1, len(path) - 1):
                    v = path[k]
                    centrality[v] += 1.0 / num_paths
    
    if n > 2:
        for v in centrality:
            centrality[v] *= 2 / ((n - 1) * (n - 2))
    
    return centrality


def eigenvector_centrality(G: AnyNxGraph) -> dict[Any, float]: 
    nodes = list(G.nodes())
    n = len(nodes)
    
    a = np.ones(n) 
    a /= np.linalg.norm(a)
    matrix = nx.adjacency_matrix(G, nodelist=nodes).toarray()

    for i in range(100):
        x = matrix.dot(a)
        norm = np.linalg.norm(x)
        if norm == 0:
            return {node : 0.0 for node in nodes}
        x /= norm
        a = x
    a = np.abs(a)
    result = {nodes[i]: float(a[i]) for i in range(n)}
    return result


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

