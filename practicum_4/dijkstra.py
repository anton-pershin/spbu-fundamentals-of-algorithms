from pathlib import Path
from queue import PriorityQueue
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
        super().__init__(G)

    def previsit(self, node: Any, **params) -> None:
        """List of params:
        * path: list[Any] (path from the initial node to the given node)
        """
        self.shortest_paths[node] = params["path"]

    def postvisit(self, node: Any, **params) -> None:
        pass

    def run(self, node: Any) -> None:

        distances = {node: float('inf') for node in self.G.nodes}
        distances[start_node] = 0
        self.shortest_paths[start_node] = [start_node]

        visited = set()
        queue = PriorityQueue()
        queue.put((0, start_node))

        while not queue.empty():
            current_distance, current_node = queue.get()

            if current_node in visited:
                continue
            visited.add(current_node)

            for neighbor in self.G.neighbors(current_node):
                weight = self.G[current_node][neighbor].get("weight", 1)
                distance = current_distance + weight

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    path = self.shortest_paths[current_node] + [neighbor]
                    self.previsit(neighbor, path=path)
                    queue.put((distance, neighbor))


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

