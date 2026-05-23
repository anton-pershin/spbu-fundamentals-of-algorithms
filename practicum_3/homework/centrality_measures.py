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
    n = G.number_of_nodes()
    centrality = {}
    for node in G:
        length = nx.shortest_path_length(G, source = node)
        total = sum(length.values())
        if total > 0:
            centrality[node] = (n-1) / total
        else:
            centrality[node] = 0

    return centrality

def betweenness_centrality(G: AnyNxGraph) -> dict[Any, float]:
    n = G.number_of_nodes()
    nodes = G.nodes()
    
    if n <= 2:
        return {node: 0.0 for node in nodes}
    
    centrality = {node: 0.0 for node in nodes}
    
    for source, target in combinations(nodes, 2):
        shortest_paths = list(nx.all_shortest_paths(G, source=source, target=target))
        num_paths = len(shortest_paths)
        
        for path in shortest_paths:
            for node in path[1:-1]:
                centrality[node] += 1.0 / num_paths

    for node in nodes:
        centrality[node] /= ((n-1) * (n-2)) / 2
    
    return centrality


def eigenvector_centrality(G: AnyNxGraph) -> dict[Any, float]:
    n = G.number_of_nodes()
    
    if n == 0:
        return {}
    if n == 1:
        return {next(G.nodes()): 1.0}
    
    nodes = list(G.nodes())
    #node_to_idx = {node: i for i, node in enumerate(nodes)} - для ручного построения A
    
    adj_matrix = nx.adjacency_matrix(G, nodelist=nodes).toarray()
    '''A = np.zeros((n, n))
    for u, v in G.edges():
        i, j = node_to_idx[u], node_to_idx[v]
        A[i, j] = 1
        A[j, i] = 1'''
    
    vector = np.ones(n)
    vector /= np.linalg.norm(vector)

    max_iterations = 100
    tolerance = 1e-6
    
    for _ in range(max_iterations):
        previous = vector.copy()
        vector = adj_matrix @ vector
        
        vector_norm = np.linalg.norm(vector)
        if vector_norm == 0:
            return {node: 0.0 for node in nodes}
        
        vector /= vector_norm
        
        if np.linalg.norm(vector - previous) < tolerance:
            return {node: float(vector[i]) for i, node in enumerate(nodes)}
    
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

