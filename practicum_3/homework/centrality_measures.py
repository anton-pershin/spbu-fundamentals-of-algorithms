from typing import Any, Protocol
from itertools import combinations
from collections import deque

import numpy as np
import networkx as nx

from src.plotting.graphs import plot_graph, plot_network_via_plotly
from src.common import AnyNxGraph 


class CentralityMeasure(Protocol):
    def __call__(self, G: AnyNxGraph) -> dict[Any, float]:
        ...


def closeness_centrality(G: AnyNxGraph) -> dict[Any, float]:

    n_total = len(G)
    if n_total <= 1:
        return {node: 0.0 for node in G.nodes()}

    graph = G.reverse() if G.is_directed() else G
    result: dict[Any, float] = {}

    for node in graph.nodes():
        lengths = nx.single_source_shortest_path_length(graph, node)
        reachable = len(lengths)
        total_dist = sum(lengths.values())

        if total_dist == 0:
            result[node] = 0.0
            continue

        value = (reachable - 1) / total_dist
        value *= (reachable - 1) / (n_total - 1)
        result[node] = float(value)

    return result

def betweenness_centrality(G: AnyNxGraph) -> dict[Any, float]: 

    nodes = list(G.nodes())
    n = len(nodes)

    if n <= 2:
        return {node: 0.0 for node in nodes}

    betweenness = {node: 0.0 for node in nodes}

    for s in nodes:
        stack = []
        predecessors = {w: [] for w in nodes}
        sigma = dict.fromkeys(nodes, 0.0)
        dist = dict.fromkeys(nodes, -1)

        sigma[s] = 1.0
        dist[s] = 0

        queue = deque([s])

        while queue:
            v = queue.popleft()
            stack.append(v)

            for w in G.neighbors(v):
                if dist[w] < 0:
                    queue.append(w)
                    dist[w] = dist[v] + 1

                if dist[w] == dist[v] + 1:
                    sigma[w] += sigma[v]
                    predecessors[w].append(v)

        delta = dict.fromkeys(nodes, 0.0)

        while stack:
            w = stack.pop()
            for v in predecessors[w]:
                if sigma[w] != 0:
                    delta[v] += (sigma[v] / sigma[w]) * (1.0 + delta[w])
            if w != s:
                betweenness[w] += delta[w]

    if not G.is_directed():
        for node in betweenness:
            betweenness[node] /= 2.0

    if G.is_directed():
        scale = 1.0 / ((n - 1) * (n - 2))
    else:
        scale = 2.0 / ((n - 1) * (n - 2))

    for node in betweenness:
        betweenness[node] *= scale

    return {node: float(value) for node, value in betweenness.items()}
   


def eigenvector_centrality(G: AnyNxGraph) -> dict[Any, float]: 

    nodes = list(G.nodes())
    n = len(nodes)

    if n == 0:
        raise nx.NetworkXPointlessConcept(
            "cannot compute centrality for the null graph"
        )

    if n == 1:
        return {nodes[0]: 1.0}

    A = nx.to_numpy_array(G, nodelist=nodes, dtype=float)
    if G.is_directed():
        A = A.T

    eigenvalues, eigenvectors = np.linalg.eig(A)

    idx = int(np.argmax(np.abs(eigenvalues)))
    vec = np.real(eigenvectors[:, idx])

    if vec.sum() < 0:
        vec = -vec

    vec = np.abs(vec)

    norm = np.linalg.norm(vec)
    if norm == 0:
        raise nx.NetworkXError("eigenvector calculation failed: zero norm eigenvector")

    vec = vec / norm

    return {node: float(vec[i]) for i, node in enumerate(nodes)}
    

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
   
