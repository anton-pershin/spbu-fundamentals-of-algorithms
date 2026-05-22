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

    result = {}
    
    for node in G.nodes():
        distances = nx.single_source_shortest_path_length(G, node)
        
        total_distance = sum(distances.values())
        
        if total_distance > 0:
            centrality = 1 / total_distance
        else:
            centrality = 0.0
        result[node] = centrality

    return result

def betweenness_centrality(G: AnyNxGraph) -> dict[Any, float]: 
    
    result = {}
    for node in G.nodes():
        result[node] = 0.0
    
    for s, t in combinations(G.nodes(), 2):
        try:
            all_paths = list(nx.all_shortest_paths(G, s, t))
        except nx.NetworkXNoPath:
            continue
        total_paths = len(all_paths)
    
        for v in G.nodes():
            if v==s or v==t:
                continue
    
            paths_through_v = 0
            for path in all_paths:
                if v in path[1:-1]:
                    paths_through_v += 1
                
            if total_paths > 0:
                result[v] += paths_through_v/total_paths
    
    
    
    return result


def eigenvector_centrality(G: AnyNxGraph) -> dict[Any, float]:
 
    centrality = {node: 1.0 for node in G.nodes()}
    
    for _ in range(100):
        new_centrality = {}
        
        for node in G.nodes():
            total = 0
            for neighbor in G.neighbors(node):
                total += centrality[neighbor]
            new_centrality[node] = total
        
        max_val = max(new_centrality.values())
        if max_val > 0:
            for node in new_centrality:
                new_centrality[node] /= max_val
        
        centrality = new_centrality
    
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

