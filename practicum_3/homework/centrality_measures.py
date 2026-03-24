from typing import Any, Protocol
from itertools import combinations

import numpy as np
import networkx as nx

from src.plotting.graphs import plot_graph, plot_network_via_plotly
from src.common import AnyNxGraph 


class CentralityMeasure(Protocol):
    def call(self, G: AnyNxGraph) -> dict[Any, float]:
        ...


def closeness_centrality(G: AnyNxGraph) -> dict[Any, float]:
    
    centrality = {}
    
    for node in G.nodes():
        distances = nx.single_source_shortest_path_length(G, node)
        sum_dist = sum(distances.values())

        if sum_dist > 0 and len(G) > 1:
            centrality[node] = 1 / sum_dist
        else:
            centrality[node] = 0.0
    
    return centrality

def betweenness_centrality(G: AnyNxGraph) -> dict[Any, float]: 

    centrality = {N: 0.0 for N in G.nodes()}
    all_nodes = list(G.nodes())

    for beginning in G.nodes():
        distances = nx.single_source_shortest_path(G, beginning)
        
        for node in G.nodes():
            if node == beginning:
                continue
            shortest_paths = list(nx.all_shortest_paths(G, beginning, node))
            total_dist = len(shortest_paths)

            for path in shortest_paths:
                for vertexes in path[1:-1]:
                    centrality[vertexes] += 1 / total_dist
    
    return centrality
    
def eigenvector_centrality(G: AnyNxGraph) -> dict[Any, float]:
    centrality = {node: 1.0 for node in G.nodes()}
    
    for i in range(100):
        centrality_new = {
            node: sum(centrality[neighbor] for neighbor in G.neighbors(node))
            for node in G.nodes()
        }
        
        norm = sum(v*v for v in centrality_new.values()) ** 0.5
        if norm == 0:
            return centrality
        
        centrality_new = {node: val / norm for node, val in centrality_new.items()}
        centrality = centrality_new
    
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
