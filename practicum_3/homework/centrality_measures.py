from typing import Any, Protocol
from itertools import combinations

import numpy as np
import networkx as nx
import scipy.sparse.linalg as la 

from src.plotting.graphs import plot_graph, plot_network_via_plotly
from src.common import AnyNxGraph 

class CentralityMeasure(Protocol):
    def __call__(self, G: AnyNxGraph) -> dict[Any, float]:
        ...

def closeness_centrality(G: AnyNxGraph) -> dict[Any, float]:
    centrality = {}
    n_nodes = G.number_of_nodes()
    
    for v in G.nodes():
        if G.degree(v) == 0:
            centrality[v] = 0.0
            continue
        try:
            sp_lengths = nx.shortest_path_length(G, source=v)
            total_distance = sum(sp_lengths[u] for u in sp_lengths if u != v)
            centrality[v] = (n_nodes - 1) / total_distance
        except nx.NetworkXNoPath:
            centrality[v] = 0.0

    return centrality

def betweenness_centrality(G: AnyNxGraph) -> dict[Any, float]: 
    centrality = {v: 0.0 for v in G.nodes()}
    nodes = list(G.nodes())
    
    for s, t in combinations(nodes, 2):
        try:
            paths = list(nx.all_shortest_paths(G, source=s, target=t))
            total_paths = len(paths)
            
            if total_paths == 0:
                continue

            for v in nodes:
                if v == s or v == t:
                    continue
                paths_through_v = sum(1 for path in paths if v in path)
                centrality[v] += paths_through_v / total_paths
        except nx.NetworkXNoPath:
            continue

    return centrality



def eigenvector_centrality(G: AnyNxGraph) -> dict[Any, float]: 
    A = nx.to_numpy_array(G)

    eigenvalues, eigenvectors = la.eigsh(A, k=1, which='LM')

    centrality_vector = np.real(eigenvectors[:, 0])

    norm = np.linalg.norm(centrality_vector)
    
    if norm > 0:
        centrality_vector_normalized = centrality_vector / norm
        if centrality_vector_normalized[0] < 0:
            centrality_vector_normalized *= -1
            
    else:
        centrality_vector_normalized = centrality_vector

    return dict(zip(G.nodes(), centrality_vector_normalized))




def plot_centrality_measure(G: AnyNxGraph, measure: CentralityMeasure) -> None:
    values = measure(G)
    if values is not None:
        plot_graph(G, node_weights=values, figsize=(14, 8), name=measure.__name__)
    else:
        print(f"Implement {measure.__name__}")

if __name__ == "__main__":
    G = nx.karate_club_graph()
    plot_centrality_measure(G, closeness_centrality)
    # plot_centrality_measure(G, nx.closeness_centrality)

    plot_centrality_measure(G, betweenness_centrality)
    # plot_centrality_measure(G, nx.betweenness_centrality)

    plot_centrality_measure(G, eigenvector_centrality)
    # plot_centrality_measure(G, nx.eigenvector_centrality)
    
    # nodes_to_check = [0, 33, 14, 20]
    
    # my_clo = closeness_centrality(G)
    # nx_clo = nx.closeness_centrality(G)
    
    # for node in nodes_to_check:
    #     print(f"node {node}: cc = {my_clo[node]:.6f}, nxcc = {nx_clo[node]:.6f}")

    # my_bet = betweenness_centrality(G)
    # nx_bet = nx.betweenness_centrality(G, normalized=False) # Без нормализации для честного сравнения
    
    # for node in nodes_to_check:
    #     print(f"node {node}: bc = {my_bet[node]:.6f}, nxbc = {nx_bet[node]:.6f}")

    # my_eig = eigenvector_centrality(G)
    
    # try:
    #     nx_eig = nx.eigenvector_centrality_numpy(G)
        
    #     for node in nodes_to_check:
    #         print(f"node {node}: ec = {my_eig[node]:.6f}, nxec = {nx_eig[node]:.6f}")
        
    # except Exception as e:
    #     print(f"err: {e}")