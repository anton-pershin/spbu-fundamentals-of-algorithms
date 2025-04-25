import sys
sys.path.append(r"/home/viktoria/algoritms/spbu-fundamentals-of-algorithms")
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
from collections import deque
from typing import Any, Protocol

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph

# Fix for colorbar bug in matplotlib
original_colorbar = plt.colorbar
def safe_colorbar(mappable, *args, **kwargs):
    kwargs.setdefault('ax', plt.gca())
    return original_colorbar(mappable, *args, **kwargs)
plt.colorbar = safe_colorbar

class CentralityMeasure(Protocol):
    def __call__(self, G: AnyNxGraph) -> dict[Any, float]:
        ...

def closeness_centrality(G: AnyNxGraph) -> dict[Any, float]:
    n = len(G)
    if n == 0:
        return {}
    closeness = {}
    for v in G:
        dist = nx.shortest_path_length(G, source=v)
        total_dist = sum(dist.values())
        if total_dist > 0.0 and n > 1:
            reachable = len(dist)
            closeness_v = (reachable - 1) / total_dist
            if reachable != n:
                closeness_v *= (reachable - 1) / (n - 1)
            closeness[v] = closeness_v
        else:
            closeness[v] = 0.0
    return closeness

def betweenness_centrality(G: AnyNxGraph) -> dict[Any, float]:
    n = len(G)
    if n == 0:
        return {}
    betweenness = dict.fromkeys(G, 0.0)
    neighbors = G.neighbors if not G.is_directed() else G.successors
    for s in G:
        S = []
        P = {v: [] for v in G}
        sigma = dict.fromkeys(G, 0.0)
        sigma[s] = 1.0
        dist = dict.fromkeys(G, -1)
        dist[s] = 0
        Q = deque([s])
        while Q:
            v = Q.popleft()
            S.append(v)
            for w in neighbors(v):
                if dist[w] < 0:
                    Q.append(w)
                    dist[w] = dist[v] + 1
                if dist[w] == dist[v] + 1:
                    sigma[w] += sigma[v]
                    P[w].append(v)
        delta = dict.fromkeys(G, 0.0)
        while S:
            w = S.pop()
            for v in P[w]:
                delta[v] += (sigma[v] / sigma[w]) * (1.0 + delta[w])
            if w != s:
                betweenness[w] += delta[w]
    if n > 2:
        scale = 1.0 / ((n - 1) * (n - 2))
        for v in betweenness:
            betweenness[v] *= scale
    return betweenness

def eigenvector_centrality(G: AnyNxGraph, max_iter: int = 100, tol: float = 1.0e-6) -> dict[Any, float]:
    n = len(G)
    if n == 0:
        return {}
    nodes = list(G)
    index_of = {v: i for i, v in enumerate(nodes)}
    A = nx.to_numpy_array(G, nodelist=nodes, dtype=float)
    x = np.full(n, 1.0 / n)
    for _ in range(max_iter):
        x_last = x
        x = A @ x_last
        norm = np.linalg.norm(x)
        if norm == 0.0:
            raise nx.NetworkXError("Eigenvector centrality failed: zero eigenvalue")
        x /= norm
        if np.linalg.norm(x - x_last, ord=1) < tol:
            break
    else:
        raise nx.NetworkXError(f"Eigenvector centrality failed to converge in {max_iter} iterations.")
    return {node: float(x[index_of[node]]) for node in nodes}

def plot_centrality_measure(G: AnyNxGraph, measure: CentralityMeasure) -> None:
    values = measure(G)
    if values is not None:
        plot_graph(G, node_weights=values, figsize=(14, 8), name=measure.__name__)
    else:
        print(f"Implement {measure.__name__}")

if __name__ == "__main__":
    G = nx.karate_club_graph()
    for measure in [closeness_centrality, betweenness_centrality, eigenvector_centrality]:
        plt.figure(figsize=(14, 8))
        plot_centrality_measure(G, measure)