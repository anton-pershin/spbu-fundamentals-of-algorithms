
import sys
import os

# (чтобы можно было импортировать из src)
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from pathlib import Path
from typing import Any
from abc import ABC, abstractmethod
import numpy as np
import networkx as nx
import heapq
from collections import deque

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

    def postvisit(self, node: Any, **params) -> None:
        pass

    def run(self, node: Any) -> None:
        self.distances = {nd: float("inf") for nd in self.G.nodes}
        self.distances[node] = 0
        priority_queue = [(0, node)]
        self.shortest_paths[node] = [node]

        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)

            if current_distance > self.distances[current_node]:
                continue

            for neighbor, weight in self.G[current_node].items():
                distance = current_distance + weight["weight"]

                if distance < self.distances[neighbor]:
                    self.distances[neighbor] = distance
                    self.shortest_paths[neighbor] =  [neighbor] + self.shortest_paths[current_node]
                    heapq.heappush(priority_queue, (distance, neighbor))


if __name__ == "__main__":
    G = nx.read_edgelist(
        Path("practicum_4") / "simple_weighted_graph_9_nodes.edgelist",
        create_using=nx.Graph
    )

    sp = DijkstraAlgorithm(G)
    sp.run("0")
    print("\n".join([f"{node}: {sp.distances[node]}" for node in sp.distances.keys()]))

    test_node = "5"
    shortest_path_edges = [
        (sp.shortest_paths[test_node][i], sp.shortest_paths[test_node][i + 1])
        for i in range(len(sp.shortest_paths[test_node]) - 1)
    ]
    plot_graph(G, highlighted_edges=shortest_path_edges)
