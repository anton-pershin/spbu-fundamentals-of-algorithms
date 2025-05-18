from typing import Any, Protocol
from collections import deque, defaultdict
import numpy as np
import networkx as nx

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class CentralityMeasure(Protocol):
    def __call__(self, G: AnyNxGraph) -> dict[Any, float]:
        ...


def bfs_shortest_paths(G: AnyNxGraph, start: Any) -> dict[Any, int]:
    visited = {start: 0}
    queue = deque([start])
    while queue:
        current = queue.popleft()
        for neighbor in G.neighbors(current):
            if neighbor not in visited:
                visited[neighbor] = visited[current] + 1
                queue.append(neighbor)
    return visited


def closeness_centrality(G: AnyNxGraph) -> dict[Any, float]:
    centrality = {}
    for node in G.nodes():
        distances = bfs_shortest_paths(G, node)
        total_distance = sum(distances.values())
        if total_distance > 0:
            centrality[node] = (len(distances) - 1) / total_distance
        else:
            centrality[node] = 0.0
    return centrality


def betweenness_centrality(G: AnyNxGraph) -> dict[Any, float]:
    betweenness = dict.fromkeys(G.nodes(), 0.0)
    for s in G.nodes():
        stack = []
        pred = defaultdict(list)
        sigma = dict.fromkeys(G.nodes(), 0.0)
        dist = dict.fromkeys(G.nodes(), -1)
        sigma[s] = 1.0
        dist[s] = 0
        queue = deque([s])
        while queue:
            v = queue.popleft()
            stack.append(v)
            for w in G.neighbors(v):
                if dist[w] < 0:
                    dist[w] = dist[v] + 1
                    queue.append(w)
                if dist[w] == dist[v] + 1:
                    sigma[w] += sigma[v]
                    pred[w].append(v)
        delta = dict.fromkeys(G.nodes(), 0.0)
        while stack:
            w = stack.pop()
            for v in pred[w]:
                delta[v] += (sigma[v] / sigma[w]) * (1 + delta[w])
            if w != s:
                betweenness[w] += delta[w]
    scale = 1 / ((len(G) - 1) * (len(G) - 2))
    for v in betweenness:
        betweenness[v] *= scale
    return betweenness


def eigenvector_centrality(G: AnyNxGraph, max_iter: int = 100, tol: float = 1e-6) -> dict[Any, float]:
    A = nx.to_numpy_array(G)
    n = A.shape[0]
    x = np.ones(n)
    for _ in range(max_iter):
        x_new = A @ x
        x_new /= np.linalg.norm(x_new)
        if np.linalg.norm(x_new - x) < tol:
            break
        x = x_new
    return {node: float(x[i]) for i, node in enumerate(G.nodes())}


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
