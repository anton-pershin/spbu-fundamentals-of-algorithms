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
    toReturn = {}
    for U in G.nodes():
        if G.degree(U):
            component = nx.node_connected_component(G, U)
            s = sum(nx.shortest_path_length(G, source=U, target=V) for V in component)
            k = (len(component)-1)/(len(G)-1)
            toReturn[U] = (len(component)-1) / float(s) * k
        else:
            toReturn[U] = 0.0
    return toReturn


# Вспомогательная функция для betweenness_centrality()
def find_all_paths(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    paths = []
    for node in set(graph.neighbors(start)) - set(path):
        paths.extend(find_all_paths(graph, node, end, path))
    return paths


def betweenness_centrality(G: AnyNxGraph) -> dict[Any, float]: 
    toReturn = {}
    for V in G.nodes():
        toReturn[V] = 0.0
        if G.degree(V):
            component = nx.node_connected_component(G, V)
            for S in component:
                for T in component:
                    if V != S and V != T and S < T:
                        all_paths = find_all_paths(G, S, T)
                        shortest_length = nx.shortest_path_length(G, source=S, target=T)
                        all_shortest_paths = list(path for path in all_paths if ((len(path)-1) == shortest_length))
                        all_shortest_paths_with_V = list(path for path in all_shortest_paths if V in path)
                        toReturn[V] += (len(all_shortest_paths_with_V)) / (len(all_shortest_paths))
            toReturn[V] *= 2/((len(G)-1)*(len(G)-2))
    return toReturn


def eigenvector_centrality(G: AnyNxGraph) -> dict[Any, float]: 
    AdjacencyMatrix = nx.to_numpy_array(G)
    Vector = np.ones(len(G))

    for i in range(1000):
        Multiplied = np.dot(AdjacencyMatrix, Vector)
        Normalized = Multiplied / np.linalg.norm(Multiplied)

        if np.linalg.norm(Normalized - Vector) < 0.00000001: break
    
        Vector = Normalized

    toReturn = {}
    for V in G.nodes():
        toReturn[V] = float(Normalized[V])
    
    return toReturn


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

