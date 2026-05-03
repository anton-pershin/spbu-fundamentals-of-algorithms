from typing import Any, Protocol
from collections import deque
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
    n_nodes = G.number_of_nodes()
    
    for node in G.nodes():
        distances = {node: 0}
        queue = deque([node])
        
        while queue:
            current = queue.popleft()
            for neighbor in G.neighbors(current):
                if neighbor not in distances:
                    distances[neighbor] = distances[current] + 1
                    queue.append(neighbor)
        
        reachable_nodes = len(distances)
        total_distance = sum(distances.values())
        
        if total_distance == 0:
            centrality[node] = 0.0
        else:
            if reachable_nodes > 1:
                centrality[node] = (reachable_nodes - 1) / (n_nodes - 1) * (1 / total_distance)
            else:
                centrality[node] = 0.0
    
    return centrality


def betweenness_centrality(G: AnyNxGraph) -> dict[Any, float]:
    centrality = {node: 0.0 for node in G.nodes()}
    n_nodes = G.number_of_nodes()
    
    for s in G.nodes():
        stack = []
        predecessors = {node: [] for node in G.nodes()}
        sigma = {node: 0 for node in G.nodes()}
        dist = {node: -1 for node in G.nodes()}  
        
        sigma[s] = 1
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
                    predecessors[w].append(v)
        
        delta = {node: 0.0 for node in G.nodes()}
        
        while stack:
            w = stack.pop()
            for v in predecessors[w]:
                delta[v] += (sigma[v] / sigma[w]) * (1 + delta[w])
            
            if w != s:
                centrality[w] += delta[w]
    
    if n_nodes > 2:
        for node in centrality:
            centrality[node] /= ((n_nodes - 1) * (n_nodes - 2))
    else:
        for node in centrality:
            centrality[node] = 0.0
    
    return centrality


def eigenvector_centrality(G: AnyNxGraph) -> dict[Any, float]:
    n_nodes = G.number_of_nodes()
    nodes = list(G.nodes())
    node_to_idx = {node: i for i, node in enumerate(nodes)}
    
    A = np.zeros((n_nodes, n_nodes))
    for u, v in G.edges():
        i, j = node_to_idx[u], node_to_idx[v]
        A[i, j] = 1
        A[j, i] = 1
    
    eigenvalues, eigenvectors = np.linalg.eig(A)
    
    max_eigenvalue_idx = np.argmax(np.real(eigenvalues))
    eigenvector = np.real(eigenvectors[:, max_eigenvalue_idx])
    
    eigenvector = np.abs(eigenvector)
    
    max_val = np.max(eigenvector)
    if max_val > 0:
        eigenvector = eigenvector / max_val
    
    centrality = {node: eigenvector[node_to_idx[node]] for node in G.nodes()}
    
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