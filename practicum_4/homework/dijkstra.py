from pathlib import Path
from typing import Any
from abc import ABC, abstractmethod
import heapq

import numpy as np
import networkx as nx

from practicum_4.dfs import GraphTraversal 
from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class DijkstraAlgorithm(GraphTraversal):
    def __init__(self, G: AnyNxGraph) -> None:
        self.shortest_paths: dict[Any, list[Any]] = {}
        super().__init__(G)

    def previsit(self, node: Any, **params) -> None:
        """List of params:
        * path: list[Any] (path from the initial node to the given node)
        """
        self.shortest_paths[node] = params["path"]

    def postvisit(self, node: Any, **params) -> None:
        pass

    def run(self, start_node: Any) -> None:
        self.distances = {node: float('inf') for node in self.G.nodes}
        self.distances[start_node] = 0
        self.shortest_paths = {start_node: [start_node]}
        heap = [(0, start_node)]
        
        while heap:
            current_dist, current_node = heapq.heappop(heap)
            if current_dist > self.distances[current_node]:
                continue
                
            for neighbor in self.G.neighbors(current_node):
                distance = current_dist + self.G.edges[current_node, neighbor].get('weight', 1)
                
                if distance < self.distances[neighbor]:
                    self.distances[neighbor] = distance
                    self.shortest_paths[neighbor] = self.shortest_paths[current_node] + [neighbor]
                    heapq.heappush(heap, (distance, neighbor))



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

