from typing import Any
from collections import deque
from itertools import combinations
import networkx as nx

def closeness_centrality(G: nx.Graph) -> dict[Any, float]:
    centrality = {}
    nodes = list(G.nodes())
    
    for node in nodes:
        distances = {n: -1 for n in nodes}
        distances[node] = 0
        queue = deque([node])
        
        while queue:
            current = queue.popleft()
            for neighbor in G.neighbors(current):
                if distances[neighbor] == -1:
                    distances[neighbor] = distances[current] + 1
                    queue.append(neighbor)
        
        total_distance = sum(d for n, d in distances.items() if n != node)
        centrality[node] = (len(nodes) - 1) / total_distance if total_distance > 0 else 0.0
    
    return centrality

def betweenness_centrality(G: nx.Graph) -> dict[Any, float]:
    nodes = list(G.nodes())
    betweenness = {n: 0.0 for n in nodes}
    
    for s, t in combinations(nodes, 2):
        try:
            all_paths = list(nx.all_shortest_paths(G, s, t))
        except nx.NetworkXNoPath:
            continue
            
        for path in all_paths:
            for node in path[1:-1]:
                betweenness[node] += 1 / len(all_paths)
    
    max_value = max(betweenness.values()) if betweenness else 1
    if max_value > 0:
        betweenness = {n: v/max_value for n, v in betweenness.items()}
    
    return betweenness

def eigenvector_centrality(G: nx.Graph, max_iter=50) -> dict[Any, float]:
    nodes = list(G.nodes())
    centrality = {n: 1.0 for n in nodes}
    
    for _ in range(max_iter):
        new_centrality = {}
        for node in nodes:
            new_centrality[node] = sum(centrality[neighbor] for neighbor in G.neighbors(node))
        
        norm = sum(new_centrality.values())
        if norm == 0:
            norm = 1
        centrality = {n: new_centrality[n]/norm for n in nodes}
    
    return centrality

