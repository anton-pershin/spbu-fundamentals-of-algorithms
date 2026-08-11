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
        distances = nx.single_source_shortest_path_length(G, node)
        if len(distances) < len(G):
            continue
        total_distance = sum(distances.values())
        if total_distance > 0:
            centrality[node] = (len(G) - 1) / total_distance
        else:
            centrality[node] = 0.0
            
    return centrality  


def betweenness_centrality(G: AnyNxGraph) -> dict[Any, float]: 
    centrality = {N: 0.0 for N in G.nodes()}
    nodes = list(G.nodes())
    
    for s, t in combinations(nodes, 2):
        try:
            paths = list(nx.all_shortest_paths(G, s, t))
        except nx.NetworkXNoPath:
            continue
        
        total_paths = len(paths)
        if total_paths == 0:
            continue
            
        for path in paths:
            for v in path[1:-1]:  
                centrality[v] += 1 / total_paths 
                
    n = len(G)
    if n > 2:
        factor = 2 / ((n - 1) * (n - 2))
        centrality = {k: v * factor for k, v in centrality.items()}                
    
    return centrality


def eigenvector_centrality(G: AnyNxGraph, max_iter=100, tolerance=1e-6) -> dict[Any, float]:
    centrality = {node: 1.0 for node in G.nodes()}
    if len(list(G.nodes())) == 0:
        return {}
    for i in range(max_iter):
        centrality_new = {
            node: sum(centrality[adj_node] for adj_node in G.neighbors(node))
            for node in G.nodes()
        }
        
        norm = sum(v*v for v in centrality_new.values()) ** 0.5
        if norm == 0:
            return centrality
        
        centrality_new = {node: val / norm for node, val in centrality_new.items()}

        difference = sum(abs(centrality_new[node] - centrality[node]) for node in G.nodes())
        if difference < tolerance:
            norm_final = sum(v*v for v in centrality_new.values()) ** 0.5
            centrality_new = {k: v / norm_final for k, v in centrality_new.items()}
            return centrality_new
        centrality = centrality_new
        
    norm_final = sum(v*v for v in centrality.values()) ** 0.5
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

