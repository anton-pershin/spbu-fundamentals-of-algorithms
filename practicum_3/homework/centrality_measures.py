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
    nodes = list(G.nodes())
    n = len(nodes)
    centrality = {}
    for v in nodes:
        path_lengths = nx.shortest_path_length(G, source=v)
        dist_sum = sum(path_lengths.values())
        if dist_sum > 0 and n > 1:
            centrality[v] = (n - 1) / dist_sum
        else:
            centrality[v] = 0.0
    return centrality

def betweenness_centrality(G: AnyNxGraph) -> dict[Any, float]: 
    nodes = list(G.nodes())
    n = len(nodes)
    centrality = {node: 0.0 for node in nodes}
    for s, t in combinations(nodes, 2):
        try:
            all_paths = list(nx.all_shortest_paths(G, s, t))
            sigma_st = len(all_paths)
            for v in nodes:
                if v == s or v == t: continue
                sigma_st_v = sum(1 for path in all_paths if v in path)
                centrality[v] += sigma_st_v / sigma_st
        except nx.NetworkXNoPath:
            continue
    if n > 2:
        scale = 2 / ((n - 1) * (n - 2))
        for v in centrality: centrality[v] *= scale
    return centrality

def eigenvector_centrality(G: AnyNxGraph) -> dict[Any, float]: 
    A = nx.to_numpy_array(G)
    eigenvalues, eigenvectors = np.linalg.eig(A)
    max_idx = np.argmax(np.real(eigenvalues))
    centrality_vector = np.abs(np.real(eigenvectors[:, max_idx]))
    norm = np.linalg.norm(centrality_vector)
    if norm != 0:
        centrality_vector = centrality_vector / norm
    nodes = list(G.nodes())
    return {nodes[i]: float(centrality_vector[i]) for i in range(len(nodes))}


def plot_centrality_measure(G: AnyNxGraph, measure: CentralityMeasure) -> None:
    values = measure(G)
    if values is not None:
        plot_graph(G, node_weights=values, name=measure.__name__)
    else:
        print(f"Implement {measure.__name__}")

if __name__ == "__main__":
    G = nx.karate_club_graph()
    
    plot_centrality_measure(G, closeness_centrality)
    plot_centrality_measure(G, betweenness_centrality)
    plot_centrality_measure(G, eigenvector_centrality)