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
    n = len(nodes)

    for start_node in nodes:
        distances = {start_node: 0}
        queue = [start_node]

        while queue:
            current = queue.pop(0)
            for neighbor in G.neighbors(current):
                if neighbor not in distances:
                    distances[neighbor] = distances[current] + 1
                    queue.append(neighbor)
        total_dist = sum(distances.values())

        if total_dist > 0:
            centrality[start_node] = (n - 1) / total_dist
        else:
            centrality[start_node] = 0.0

    return centrality


def betweenness_centrality(G: AnyNxGraph) -> dict[Any, float]:
    betweenness = {node: 0.0 for node in G.nodes()}
    nodes = list(G.nodes())

    for s in nodes:
        S = []
        pred = {v: [] for v in nodes}
        sigma = {v: 0 for v in nodes};
        sigma[s] = 1
        dist = {v: -1 for v in nodes};
        dist[s] = 0
        queue = [s]

        while queue:
            v = queue.pop(0)
            S.append(v)
            for w in G.neighbors(v):
                if dist[w] < 0:
                    dist[w] = dist[v] + 1
                    queue.append(w)
                if dist[w] == dist[v] + 1:
                    sigma[w] += sigma[v]
                    pred[w].append(v)

        delta = {v: 0 for v in nodes}
        while S:
            w = S.pop()
            for v in pred[w]:
                delta[v] += (sigma[v] / sigma[w]) * (1 + delta[w])
            if w != s:
                betweenness[w] += delta[w]

    n = len(nodes)
    norm = (n - 1) * (n - 2) / 2
    for v in betweenness:
        betweenness[v] /= norm

    return betweenness


def eigenvector_centrality(G: AnyNxGraph) -> dict[Any, float]:
    nodes = list(G.nodes())
    n = len(nodes)

    x = {node: 1.0 / n for node in nodes}

    max_iter = 100
    tol = 1.0e-6

    for _ in range(max_iter):
        x_last = x.copy()

        for node in nodes:
            total = sum(x_last[neighbor] for neighbor in G.neighbors(node))
            x[node] = total

        norm = np.sqrt(sum(v ** 2 for v in x.values()))
        if norm == 0:
            return {node: 0.0 for node in nodes}

        for node in x:
            x[node] /= norm

        error = sum(abs(x[node] - x_last[node]) for node in nodes)
        if error < tol:
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

