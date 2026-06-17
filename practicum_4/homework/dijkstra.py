from pathlib import Path
from typing import Any
from abc import ABC, abstractmethod

import numpy as np
import networkx as nx
import heapq

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
        self.visited = set()
        self.distances = {node: 0}
        priority_queue = [(0, node, [node])]

        while priority_queue:
            current_distance, cur, current_path = heapq.heappop(priority_queue)
            if cur in self.visited:
                continue

            self.visited.add(cur)
            self.previsit(cur, path=current_path)

            for neighbor in self.G.neighbors(cur):
                if neighbor not in self.visited:
                    edge_weight = self.G[cur][neighbor].get('weight', 1)
                    new_distance = current_distance + edge_weight

                    if neighbor not in self.distances or new_distance < self.distances[neighbor]:
                        self.distances[neighbor] = new_distance
                        new_path = current_path + [neighbor]
                        heapq.heappush(priority_queue, (new_distance, neighbor, new_path))


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

