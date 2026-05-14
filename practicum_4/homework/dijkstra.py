from pathlib import Path
from typing import Any
from abc import ABC, abstractmethod

import numpy as np
import networkx as nx

from practicum_4.dfs import GraphTraversal 
from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


import heapq

import heapq

class DijkstraAlgorithm(GraphTraversal):
    def __init__(self, G: AnyNxGraph) -> None:
        self.shortest_paths: dict[Any, list[Any]] = {}
        super().__init__(G)

    def previsit(self, node: Any, **params) -> None:
        
        self.shortest_paths[node] = params["path"]

    def postvisit(self, node: Any, **params) -> None:

        pass

    def run(self, start_node: Any) -> None:
        pq = [(0, start_node, [start_node])]
        distances = {node: float('inf') for node in self.G.nodes}
        distances[start_node] = 0
        visited = set()

        while pq:
            current_dist, u, path = heapq.heappop(pq)
            
            if u not in visited:
                visited.add(u)
                self.previsit(u, path=path)
                
                for neighbor in self.G.neighbors(u):
                    weight = self.G[u][neighbor].get("weight", 1)
                    distance = current_dist + weight
                    
                    if distance < distances[neighbor]:
                        distances[neighbor] = distance
                        new_path = path + [neighbor]
                        heapq.heappush(pq, (distance, neighbor, new_path))


if __name__ == "__main__":
    G = nx.read_edgelist(
        Path("practicum_4") / "simple_weighted_graph_9_nodes.edgelist",
        create_using=nx.Graph
    )
    plot_graph(G)

    sp = DijkstraAlgorithm(G)
    sp.run("0")

    test_node = "5"
    shortest_path_edges = [
        (sp.shortest_paths[test_node][i], sp.shortest_paths[test_node][i + 1])
        for i in range(len(sp.shortest_paths[test_node]) - 1)
    ]
    plot_graph(G, highlighted_edges=shortest_path_edges)

