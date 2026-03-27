import sys
sys.path.insert(0, r"C:\projects\cpp_proj\cpp_beg\cppvs\algorithms\spbu-fundamentals-of-algorithms")

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
    n = len(G)
    
    
    for node in G.nodes():
        

        lengths = nx.single_source_shortest_path_length(G, node)
        
        sum_distances = sum(lengths[target] for target in G.nodes() if target != node)
        
        if sum_distances > 0:
            closeness[node] = (n - 1) / sum_distances 
        else:
            closeness[node] = 0.0
    
    return closeness


def betweenness_centrality(G: AnyNxGraph) -> dict[Any, float]: 

    betweenness = {node: 0.0 for node in G.nodes()}
    
    for s, t in combinations(G.nodes(), 2):
        try:
            # σ(s, t) - общее кол-во кратчайших путей
            shortest_paths = list(nx.all_shortest_paths(G, s, t))
            sigma_st = len(shortest_paths)
        except nx.NetworkXNoPath:
            continue
        
        # Для каждой вершины v (где v ≠ s и v ≠ t)
        for v in G.nodes():
            if v == s or v == t:
                continue
            
            # σ(s, t | v) - кол-во кратчайших путей, проходящих через v
            sigma_st_v = sum(1 for path in shortest_paths if v in path)
            
            # Добавляем к централности: σ(s, t | v) / σ(s, t)
            betweenness[v] += sigma_st_v / sigma_st
    
    n = len(G)
    for node in betweenness:
        betweenness[node] = betweenness[node] * 2 / ((n - 1) * (n - 2))
    
    return betweenness


def eigenvector_centrality(G: AnyNxGraph) -> dict[Any, float]: 

    try:

        A = nx.adjacency_matrix(G)
        
        eigenvalues, eigenvectors = np.linalg.eig(A.toarray())
        

        max_eigenvalue_idx = np.argmax(eigenvalues)
        centrality_vector = np.real(eigenvectors[:, max_eigenvalue_idx])


        centrality_vector = np.abs(centrality_vector)
        centrality_vector = centrality_vector / np.max(centrality_vector)
        
        nodes = list(G.nodes())
        result = {nodes[i]: float(centrality_vector[i]) for i in range(len(nodes))}
        
        return result
    except Exception:
        return None


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

