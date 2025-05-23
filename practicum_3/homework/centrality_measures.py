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
    centrality = {}
    nodes = G.nodes()
    num_nodes = len(nodes)

    for node in nodes:
        paths = nx.single_source_shortest_path_length(G, node).values()
        total_dist = sum(paths)
        closeness = (num_nodes - 1) / total_dist if total_dist > 0 else 0

        centrality[node] = closeness
        
    return centrality



def betweenness_centrality(G: AnyNxGraph) -> dict[Any, float]:
    centrality = {}
    nodes = G.nodes()
    for node in nodes:
        centrality[node] = 0

    for start_node in nodes:
        stack = []
        sigma = {n: 0 for n in nodes}
        pred = {n: [] for n in nodes}
        sigma[start_node] = 1
        dist = {n: -1 for n in nodes}
        dist[start_node] = 0
        queue = deque([start_node])
        
        while len(queue) > 0:
            current_node = queue.popleft()
            stack.append(current_node)
            for neighbor in G.neighbors(current_node):
                if dist[neighbor] < 0:
                    queue.append(neighbor)
                    dist[neighbor] = dist[current_node] + 1
                if dist[neighbor] == dist[current_node] + 1:
                    sigma[neighbor] += sigma[current_node]
                    pred[neighbor].append(current_node)
        
        delta = {n: 0 for n in nodes}
        while len(stack) > 0:
            w = stack.pop()
            for u in pred[w]:
                delta[u] += (sigma[u] / sigma[w]) * (1 + delta[w])
            if w != start_node:
                centrality[w] += delta[w]
    
    for node in nodes:
        centrality[node] /= 2
    
    return centrality



def eigenvector_centrality(G: AnyNxGraph) -> dict[Any, float]:
    centrality = {}
    nodes = list(G.nodes())
    A = nx.to_numpy_array(G, nodelist=nodes)
    x = np.ones(len(nodes))
    for _ in range(100):
        x_new = A @ x
        x_new /= np.linalg.norm(x_new, 2)
        if np.linalg.norm(x_new - x, 2) < 1e-6:
            x = x_new.tolist()
            break
        x = x_new
    for index, node in enumerate(nodes):
        centrality[node] = x[index]
    return centrality



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