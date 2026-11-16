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
    n = len(G)
    H = G.reverse(copy=False) if G.is_directed() else G
    result = {}
    for v in G:
        dist = nx.single_source_shortest_path_length(H, v)
        total = sum(dist.values())
        reachable = len(dist) - 1
        if total > 0 and n > 1:
            result[v] = (reachable / total) * (reachable / (n - 1))
        else:
            result[v] = 0.0
    return result


def betweenness_centrality(G: AnyNxGraph) -> dict[Any, float]: 
    bc = dict.fromkeys(G, 0.0)
    for s in G:
        stack = []
        preds = {v: [] for v in G}
        sigma = dict.fromkeys(G, 0.0)
        sigma[s] = 1.0
        dist = {s: 0}
        queue = [s]
        head = 0
        while head < len(queue):
            v = queue[head]
            head += 1
            stack.append(v)
            for w in G[v]:
                if w not in dist:
                    dist[w] = dist[v] + 1
                    queue.append(w)
                if dist[w] == dist[v] + 1:
                    sigma[w] += sigma[v]
                    preds[w].append(v)
        delta = dict.fromkeys(G, 0.0)
        while stack:
            w = stack.pop()
            for v in preds[w]:
                delta[v] += sigma[v] / sigma[w] * (1.0 + delta[w])
            if w != s:
                bc[w] += delta[w]
    n = len(G)
    if n > 2:
        scale = 1.0 / ((n - 1) * (n - 2))
        for v in bc:
            bc[v] *= scale
    return bc


def eigenvector_centrality(G: AnyNxGraph) -> dict[Any, float]: 
    nodes = list(G)
    A = nx.to_numpy_array(G, nodelist=nodes, weight=None)
    if G.is_directed():
        A = A.T  
    M = A + np.eye(len(nodes))
    x = np.ones(len(nodes)) / np.sqrt(len(nodes))
    for _ in range(10000):
        x_new = M @ x
        x_new /= np.linalg.norm(x_new)
        if np.linalg.norm(x_new - x) < 1e-12:
            x = x_new
            break
        x = x_new
    return dict(zip(nodes, x))


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

