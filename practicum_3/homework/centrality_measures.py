from typing import Any, Protocol
from itertools import combinations

import sys
from pathlib import Path
project_root = Path(__file__).absolute().parents[2]
sys.path.insert(0, str(project_root))


import numpy as np
import networkx as nx

from src.plotting.graphs import plot_graph, plot_network_via_plotly
from src.common import AnyNxGraph 

class CentralityMeasure(Protocol):
    def __call__(self, G: AnyNxGraph) -> dict[Any, float]:
        ...

def closeness_centrality(G: nx.Graph) -> dict[Any, float]:
    centrality = {}
    nodes = list(G.nodes())
    n = len(nodes)
    for node in nodes:
        total_distance = sum(nx.shortest_path_length(G, source=node).values())
        centrality[node] = (n - 1) / total_distance
    return centrality

def betweenness_centrality(G: nx.Graph) -> dict[Any, float]:
    centrality = {n: 0.0 for n in G.nodes()}
    nodes = list(G.nodes())
    n = len(nodes)
    for s, t in combinations(nodes, 2):
        sigma_st = len(list(nx.all_shortest_paths(G, s, t)))
        for v in nodes:
            if v != s and v != t:          
                dist_st = nx.shortest_path_length(G, s, t)
                dist_sv = nx.shortest_path_length(G, s, v)
                dist_vt = nx.shortest_path_length(G, v, t)
                if dist_sv + dist_vt == dist_st:      
                    sigma_sv = len(list(nx.all_shortest_paths(G, s, v)))
                    sigma_vt = len(list(nx.all_shortest_paths(G, v, t)))
                    centrality[v] += (sigma_sv * sigma_vt) / sigma_st
    return centrality # значения отличаются от функции в nx тк не юзаем scale; в nx каждый элемент умножается на 2/((n-1)*(n-2))

def eigenvector_centrality(G: AnyNxGraph) -> dict[Any, float]:
    centrality = {}
    nodes = list(G.nodes())
    eigenvalues, eigenvectors = np.linalg.eigh(nx.adjacency_matrix(G).todense().astype(float))
    major_eigenvector = np.abs(eigenvectors[:, np.argmax(np.abs(eigenvalues))].flatten())
    for i in range(len(nodes)):
        centrality[nodes[i]] = float(major_eigenvector[i])
    return centrality # достаточно близкие значения

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
