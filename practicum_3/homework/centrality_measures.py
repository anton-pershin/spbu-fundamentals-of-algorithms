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
    centrs = {}
    n = len(G)

    for v in G.nodes():  
        length = nx.single_source_shortest_path_length(G,v)
        dist = sum(length.values())

        if dist == 0:
            centrs[v] = 0.0
        else: 
            centrs[v] = 1 / dist 
    
    return centrs

def betweenness_centrality(G: AnyNxGraph) -> dict[Any, float]: 
    centrs = {v: 0.0 for v in G.nodes()}
    nodes= list(G.nodes())

    for s,t in combinations(nodes, 2):
        len_from_s = nx.single_source_shortest_path_length(G,s)
        len_from_t = nx.single_source_shortest_path_length(G,t)
        d_st = len_from_s[t]
        paths = list(nx.all_shortest_paths(G,s,t))
        num = len(paths)
        for v in nodes:
            if s != v and t != v :
                d_sv = len_from_s[v]
                d_vt = len_from_t[v]
                if d_sv + d_vt == d_st:
                    centrs[v] += 1.0/num
    return centrs


def eigenvector_centrality(G: AnyNxGraph) -> dict[Any, float]: 
    nodes = list(G.nodes())
    n = len(nodes)
    A = nx.adjacency_matrix(G, nodelist=nodes).toarray()
    c = np.ones(n)
    for x in range(1000):
        c_new = np.zeros(n)
        for i in range(n):
            total = 0
            for j in range(n):
                total += A[i][j] * c[j]
            c_new[i]= total
        norm = np.linalg.norm(c_new)
        if norm != 0:
            c_new = c_new / norm
        c = c_new
    res = {nodes[i] : float(c[i]) for i in range(n)}
    return res


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

