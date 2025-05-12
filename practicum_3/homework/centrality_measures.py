from typing import Any, Protocol
from itertools import combinations
from heapq import heappop, heappush
from collections import defaultdict

import numpy as np
import networkx as nx

from src.plotting.graphs import plot_graph, plot_network_via_plotly
from src.common import AnyNxGraph
from src.linalg import get_numpy_eigenvalues, get_scipy_solution


class CentralityMeasure(Protocol):
    def __call__(self, G: AnyNxGraph) -> dict[Any, float]:
        ...


def closeness_centrality(G: AnyNxGraph) -> dict[Any, float]:
    def dijkstra(graph: AnyNxGraph, source: Any) -> dict[Any, float]:
        distance = {node: float('inf') for node in graph.nodes}
        distance[source] = 0

        # Priority queue to select node with smallest distance
        queue = [(0, source)]

        while queue:
            current_distance, current_node = heappop(queue)

            if current_distance > distance[current_node]:
                continue
            for neighbor, attributes in graph[current_node].items():
                weight = attributes.get("weight", 1)
                distance_to_neighbor = current_distance + weight

                if distance_to_neighbor < distance[neighbor]:
                    distance[neighbor] = distance_to_neighbor
                    heappush(queue, (distance_to_neighbor, neighbor))

        return distance
    
    
    node_closeness_centrality = dict()
    n = len(G)
    for node in range(n):
        dist_array = dijkstra(G, node)
        node_closeness_centrality[node] = (1 / sum([dist_array[i] for i in range(n)]))
    return node_closeness_centrality



def betweenness_centrality(G: AnyNxGraph) -> dict[Any, float]:
    def dijkstra_all_paths(graph, start):
        distances = {node: float('inf') for node in graph.nodes()}
        distances[start] = 0
        predecessors = defaultdict(list)
        heap = [(0, start)]
        
        while heap:
            current_dist, u = heappop(heap)
            if current_dist > distances[u]:
                continue
            for v in graph.neighbors(u):
                new_dist = current_dist + 1
                if new_dist < distances[v]:
                    distances[v] = new_dist
                    predecessors[v] = [u]
                    heappush(heap, (new_dist, v))
                elif new_dist == distances[v]:
                    predecessors[v].append(u)
        return distances, predecessors
    
    def get_all_paths(predecessors, start, end):
        paths = []
        def dfs(node, path):
            if node == start:
                paths.append(list(reversed(path)))
                return
            for pred in predecessors[node]:
                dfs(pred, path + [pred])
        dfs(end, [end])
        return paths


    node_betweenness_centrality = dict()
    all_paths = dict()
    n = len(G)
    for start_node in range(n):
        distances, predcessors = dijkstra_all_paths(G, start_node)
        all_paths_from_node = [get_all_paths(predcessors, start_node, end_node) for end_node in range(n)]
        all_paths[start_node] = all_paths_from_node
    
    for bridge_node in range(n):
        sigma = 0
        for s in range(n):
            for t in range(s+1, n):
                if (bridge_node != s and bridge_node != t):
                    shortest_paths, shortest_paths_with_bridge = 0, 0
                    for path in all_paths[s][t]:
                        if bridge_node in path:
                            shortest_paths_with_bridge +=1
                        shortest_paths +=1
                    sigma += shortest_paths_with_bridge / shortest_paths
        node_betweenness_centrality[bridge_node] = sigma
    return node_betweenness_centrality
    

def eigenvector_centrality(G: AnyNxGraph) -> dict[Any, float]: 
    def find_dominant_eigenvector(A, max_iter=100, tol=1e-6):
        eigenvalues = get_numpy_eigenvalues(A)
        lambda_max = np.max(eigenvalues.real)
        
        sigma = lambda_max + 1e-3  
        
        n = A.shape[0]
        v = np.random.rand(n)
        v /= np.linalg.norm(v)
        
        A_shifted = A - sigma * np.identity(n)
        
        for _ in range(max_iter):
            v_new = get_scipy_solution(A_shifted, v)
            v_new /= np.linalg.norm(v_new)
            
            # Проверяем сходимость
            if np.linalg.norm(v_new - v) < tol:
                break
            
            v = v_new
        
        return v

    node_eigenvector_centrality = dict()

    v = find_dominant_eigenvector(nx.adjacency_matrix(G).toarray())

    for node in range(len(G)):
        node_eigenvector_centrality[node] = v[node]
    return node_eigenvector_centrality



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

