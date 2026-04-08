from typing import Any, Protocol
from itertools import combinations

import numpy as np
import networkx as nx
import math

from src.plotting.graphs import plot_graph, plot_network_via_plotly
from src.common import AnyNxGraph 


class CentralityMeasure(Protocol):
    def __call__(self, G: AnyNxGraph) -> dict[Any, float]:
        ...


def closeness_centrality(G: AnyNxGraph) -> dict[Any, float]:
    if type(G) in [nx.DiGraph, nx.MultiDiGraph]:
        G = G.reverse() 
    N = G.number_of_nodes()
    result_list = []    

    for node in G:
        current_component = nx.shortest_path_length(G, node)
        n = len(current_component)
        count = sum(current_component.values())

        if n > 1:
            result_list.append((node, float(((n-1) / (N-1)) * ((n - 1) / count))))
        if n == 1:
            result_list.append((node, 0.0))

    result_dict = dict(result_list)
    return result_dict

def betweenness_centrality(G: AnyNxGraph) -> dict[Any, float]: 
    N = G.number_of_nodes()
    result = {node: 0.0 for node in G}
    if N <= 2: return result
    
    for s in G.nodes():
        for t in G.nodes():
            if s == t: continue
            if not G.is_directed() and s >= t: continue

            try:
                paths = list(nx.all_shortest_paths(G, s, t))
            except nx.NetworkXNoPath:
                continue

            if not paths: continue

            total = len(paths)

            for path in paths:
                nodes_in_path = path[1:-1]
                for v in nodes_in_path:
                    result[v] += 1.0 / total

    for v in result:
        if G.is_directed():
            result[v] = result[v] / ((N-1)*(N-2))
        else:
            result[v] = result[v] / ((N-1)*(N-2) / 2)

    return result

def eigenvector_centrality(G: AnyNxGraph) -> dict[Any, float]:
    if len(G) == 0: return {}
    
    nstart = {v: 1 for v in G}
    
    if all(v == 0 for v in nstart.values()):
        return {v: 0 for v in G}
    
    nstart_sum = sum(nstart.values())
    x = {k: v / nstart_sum for k, v in nstart.items()}
    
    nnodes = G.number_of_nodes()
    
    for _ in range(100):
        xlast = x
        x = xlast.copy()
        
        for n in x:
            for nbr in G[n]:
                x[nbr] += xlast[n]
        
        norm = math.hypot(*x.values())
        if norm == 0:
            norm = 1
        x = {k: v / norm for k, v in x.items()}
        
        diff = sum(abs(x[n] - xlast[n]) for n in x)
        if diff < nnodes * 1e-6:
            break
    
    return x


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