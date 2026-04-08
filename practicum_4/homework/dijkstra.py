from pathlib import Path
from typing import Any
from abc import ABC, abstractmethod

import numpy as np
import networkx as nx

from practicum_4.dfs import GraphTraversal 
from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph

class DijkstraAlgorithm(GraphTraversal):
    def __init__(self, G: AnyNxGraph) -> None:
        self.shortest_paths: dict[Any, list[Any]] = {}
        self.distances: dict[Any, float] = {}
        super().__init__(G)

    def previsit(self, node: Any, **params) -> None:
        self.shortest_paths[node] = params["path"]
        self.distances[node] = params["distance"]

    def postvisit(self, node: Any, **params) -> None:
        print(f"Вершина {node} обработана. Кратчайшее расстояние: {self.distances.get(node, 'inf')}")

    def run(self, node: Any) -> None:

        dist = {v: float('inf') for v in self.G.nodes()}
        dist[node] = 0
        prev = {v: None for v in self.G.nodes()}
        processed = set()
        
        while len(processed) < len(self.G.nodes()):
            current = None
            min_dist = float('inf')
            for v in self.G.nodes():
                if v not in processed and dist[v] < min_dist:
                    min_dist = dist[v]
                    current = v
            
            if current is None or min_dist == float('inf'):
                break
            
            path = []
            temp = current
            while temp is not None:
                path.append(temp)
                temp = prev[temp]
            path.reverse()
            
            self.previsit(current, path=path, distance=min_dist)
            
            processed.add(current)
            
            for neighbor in self.G.neighbors(current):
                if neighbor not in processed:
                    weight = self.G[current][neighbor].get('weight', 1)
                    new_dist = min_dist + weight
                    
                    if new_dist < dist[neighbor]:
                        dist[neighbor] = new_dist
                        prev[neighbor] = current
            
            self.postvisit(current)

if __name__ == "__main__":
    G = nx.read_edgelist(
        Path("practicum_4") / "simple_weighted_graph_9_nodes.edgelist",
        create_using=nx.Graph
    )
    plot_graph(G)

    sp = DijkstraAlgorithm(G)
    sp.run("0")

    print("\n=== КРАТЧАЙШИЕ ПУТИ ===")
    for node, path in sp.shortest_paths.items():
        distance = sp.distances.get(node, float('inf'))
        if distance != float('inf'):
            print(f"{node}: {' -> '.join(map(str, path))} (расстояние = {distance})")
        else:
            print(f"{node}: недостижима")

    test_node = "5"
    if test_node in sp.shortest_paths:
        shortest_path_edges = [
            (sp.shortest_paths[test_node][i], sp.shortest_paths[test_node][i + 1])
            for i in range(len(sp.shortest_paths[test_node]) - 1)
        ]
        print(f"\nПуть от 0 до {test_node}: {sp.shortest_paths[test_node]}")
        print(f"Расстояние: {sp.distances[test_node]}")
        plot_graph(G, highlighted_edges=shortest_path_edges)

