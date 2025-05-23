from typing import Any, Protocol
from itertools import combinations
import matplotlib.pyplot as plt
original_colorbar = plt.colorbar
from collections import deque
import sys
sys.path.append(r"C:\Users\vital\OneDrive\Документы\GitHub\spbu-fundamentals-of-algorithms-2")
"""
У меня Windows и я не смог запустить иначе, ну совсем никак. Рискну предположить, что Вам необходимо убрать строчку sys.path.append
Она нужна для того чтобы программа видела src и всё что внутри. 
Кроме этого у вас ошибка в plotting/graphs.py.
Если поменять:
plt.colorbar(sm)
на:
plt.colorbar(sm, ax=plt.gca())
то заработает без "Хаков", по типу plt.colorbar
я попытался сделать хорошо, но к дедлайну успел чтобы просто работало....
"""
import numpy as np
import networkx as nx

from src.plotting.graphs import plot_graph, plot_network_via_plotly
from src.common import AnyNxGraph 

def safe_colorbar(mappable, *args, **kwargs):
    kwargs.setdefault('ax', plt.gca())
    return original_colorbar(mappable, *args, **kwargs)
plt.colorbar = safe_colorbar

from src.plotting.graphs import plot_graph, plot_network_via_plotly

class CentralityMeasure(Protocol):
    def __call__(self, G: AnyNxGraph) -> dict[Any, float]:
        ...

def closeness_centrality(G: AnyNxGraph) -> dict[Any, float]:
    n = len(G)
    if n == 0:
        return {}

    closeness: dict[Any, float] = {}

    for v in G:
        dist: dict[Any, float] = nx.shortest_path_length(G, source=v, weight=None)
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
        S: list[Any] = []
        P = {v: [] for v in G}
        sigma = dict.fromkeys(G, 0.0)
        sigma[s] = 1.0
        dist = dict.fromkeys(G, -1)
        dist[s] = 0

        Q: deque[Any] = deque([s])

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
                delta_v = (sigma[v] / sigma[w]) * (1.0 + delta[w])
                delta[v] += delta_v
            if w != s:
                betweenness[w] += delta[w]

    if n > 2:
        if not G.is_directed():
            scale = 1.0 / ((n - 1) * (n - 2))
        else:
            scale = 1.0 / ((n - 1) * (n - 2))
        for v in betweenness:
            betweenness[v] *= scale

    return betweenness


def eigenvector_centrality(
    G: AnyNxGraph,
    max_iter: int = 100, # надо ли это?
    tol: float = 1.0e-6,  # надо ли это?
) -> dict[Any, float]:
    n = len(G)
    if n == 0:
        return {}

    index_of = {v: i for i, v in enumerate(G)}
    nodes = list(G)

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
        raise nx.NetworkXError(
            f"Eigenvector centrality failed to converge in {max_iter} iterations."
        )

    return {node: float(x[index_of[node]]) for node in nodes}




def plot_centrality_measure(G: AnyNxGraph, measure: CentralityMeasure) -> None:
    values = measure(G)
    if values is not None:
        plot_graph(G, node_weights=values, figsize=(14, 8), name=measure.__name__)
    else:
        print(f"Implement {measure.__name__}")
"""
проверял одну функцию, прошу прощения, но я оставлю эти строки пока не разберусь.
if __name__ == "__main__":
    G = nx.karate_club_graph()

    my_vals = betweenness_centrality(G)
    nx_vals = nx.betweenness_centrality(G, normalized=True)
    for key in my_vals:
        print(f"{key}: my={my_vals[key]}, nx={nx_vals[key]}, diff={my_vals[key]-nx_vals[key]}")
    
    assert np.allclose(
        [my_vals[k] for k in sorted(my_vals)],
        [nx_vals[k] for k in sorted(nx_vals)],
        atol=1e-12,
    )
"""
if __name__ == "__main__":
    G = nx.karate_club_graph()

    plt.figure(figsize=(14, 8))
    plot_centrality_measure(G, closeness_centrality)
    plt.figure(figsize=(14, 8))
    plot_centrality_measure(G, betweenness_centrality)
    plt.figure(figsize=(14, 8))
    plot_centrality_measure(G, eigenvector_centrality)