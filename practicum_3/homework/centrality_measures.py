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
    nodes = list(G.nodes())
    n = len(nodes)
    res = {}

    for u in nodes:
        lengths = nx.single_source_shortest_path_length(G, u)
        sum_dist = sum(lengths.values())
        
        if sum_dist > 0:
            reachable_nodes = len(lengths) - 1
            if reachable_nodes > 0:
                norm = reachable_nodes / (n - 1)
                res[u] = (reachable_nodes / sum_dist) * norm
            else:
                res[u] = 0.0
        else:
            res[u] = 0.0
            
    return res


def betweenness_centrality(G: AnyNxGraph) -> dict[Any, float]: 
    nodes = list(G.nodes())
    n = len(nodes)
    between = {node: 0.0 for node in nodes}
    
    for s, t in combinations(nodes, 2):
        try:
            all_paths = list(nx.all_shortest_paths(G, source=s, target=t))
            sigma_st = len(all_paths)
            
            for v in nodes:
                if v != s and v != t:
                    sigma_v = 0
                    for path in all_paths:
                        if v in path:
                            sigma_v += 1
                    
                    between[v] += sigma_v / sigma_st
        except nx.NetworkXNoPath:
            pass

    if n > 2:
        coeff = 2.0 / ((n - 1) * (n - 2))
        for node in between:
            between[node] *= coeff
            
    return between


def eigenvector_centrality(G: AnyNxGraph) -> dict[Any, float]: 
    nodes = list(G.nodes())
    n = len(nodes)
    
    adj = nx.to_numpy_array(G, nodelist=nodes)
    
    x = np.ones(n)
    
    for _ in range(100):
        prev_x = x.copy()
        
        x = adj @ x
        
        norm = np.linalg.norm(x)
        if norm > 0:
            x = x / norm
        
        if np.allclose(x, prev_x, atol=1e-6):
            break
            
    return {nodes[i]: float(x[i]) for i in range(n)}


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