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

    centrality = {}

    for node in G.nodes():
        distances = nx.shortest_path_length(G, source=node)

        total_distance = sum(dist for target, dist in distances.items()
                                  if target != node)
        
        if total_distance > 0:
            centrality[node] = 1 / total_distance
        else:
            centrality[node] = 0

    return centrality


def betweenness_centrality(G: AnyNxGraph) -> dict[Any, float]: 

    betweenness = {node: 0.0 for node in G.nodes()}
    nodes = list(G.nodes())
    
    for s in nodes:
        for t in nodes:
            if s >= t:
                continue
                
            try:
                all_paths = list(nx.all_shortest_paths(G, source=s, target=t))
                total_paths = len(all_paths)
                
                for path in all_paths:
                    for v in path[1:-1]:
                        betweenness[v] += 1 / total_paths
            except nx.NetworkXNoPath:
                continue
    
    n = len(nodes)
    if n > 2:
        for node in betweenness:
            betweenness[node] = betweenness[node] / ((n-1)*(n-2))
    
    return betweenness


def eigenvector_centrality(G: AnyNxGraph) -> dict[Any, float]: 

    A = nx.adjacency_matrix(G).astype(float)
    
    eigenvalues, eigenvectors = np.linalg.eig(A.toarray())
    
    max_index = np.argmax(eigenvalues)
    eigenvector = np.abs(eigenvectors[:, max_index])
    
    eigenvector = eigenvector / np.max(eigenvector)
    
    centrality = {node: eigenvector[i] for i, node in enumerate(G.nodes())}
    
    return centrality


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

