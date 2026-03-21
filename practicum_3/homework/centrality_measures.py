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

    return result+

def betweenness_centrality(G: AnyNxGraph) -> dict[Any, float]: 

    pass


def eigenvector_centrality(G: AnyNxGraph) -> dict[Any, float]: 

    ##########################
    ### PUT YOUR CODE HERE ###
    #########################

    pass


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

