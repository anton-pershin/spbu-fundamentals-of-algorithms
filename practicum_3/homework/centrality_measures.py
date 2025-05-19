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
    nodes = list(G.nodes())
    for node in nodes:
        path = nx.shortest_path_length(G, source=node)
        sum_of_dist = sum(path.values())
        centrality[node] = (len(nodes) - 1) / sum_of_dist
    return centrality


def betweenness_centrality(G: AnyNxGraph) -> dict[Any, float]: 
    centrality = {v: 0.0 for v in G.nodes()}
    nodes = list(G.nodes())
    s_list = []

    for t in nodes:
        for s in s_list:
            path_without_v = len(list(nx.all_shortest_paths(G, s, t)))
            for v in nodes:
                if v != s and v != t:
                    sv = nx.shortest_path_length(G, s, v)
                    vt = nx.shortest_path_length(G, v, t)
                    st = nx.shortest_path_length(G, s, t)
                    if sv + vt == st:
                        path_sv = len(list(nx.all_shortest_paths(G, s, v)))
                        path_vt = len(list(nx.all_shortest_paths(G, v, t)))
                        centrality[v] += (path_sv * path_vt) / path_without_v
        s_list.append(t)



def eigenvector_centrality(G: AnyNxGraph) -> dict[Any, float]:

    pass


def plot_centrality_measure(G: AnyNxGraph, measure: CentralityMeasure) -> None:
    values = measure(G)
    if values is not None:
        plot_graph(G, node_weights=values, figsize=(14, 8), name=measure.__name__)
    else:
        print(f"Implement {measure.__name__}")


if __name__ == "__main__":
    G = nx.karate_club_graph()
    #plot_graph(G)
    plot_centrality_measure(G, closeness_centrality)
    plot_centrality_measure(G, betweenness_centrality)
    plot_centrality_measure(G, eigenvector_centrality)


