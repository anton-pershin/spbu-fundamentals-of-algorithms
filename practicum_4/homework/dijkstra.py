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
        self.shortest_paths[node] = params["path"]

    def postvisit(self, node: Any, **params) -> None:
        pass

    def _restore_path(self, parents : dict, end : Any) -> list:

        path = []
        start = end

        while start is not None:
            path.append(start)
            start = parents[start]
        path.reverse()

        return path
    
    def run(self, start_node: Any) -> None:

        distances = {node: float("inf") for node in self.G.nodes()}
        distances[start_node] = 0
        parent = {node: None for node in self.G.nodes()}

        min_dist_queue = [(0, start_node)]
        
        while min_dist_queue:
            current_dist, current = heapq.heappop(min_dist_queue)

            if current_dist > distances[current]:
                continue

            for neighbor, edge_info in self.G[current].items():
                if "weight" in edge_info:
                    weight = edge_info["weight"]
                else:
                    weight = 1
                new_dist = current_dist + weight

                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    parent[neighbor] = current
                    heapq.heappush(min_dist_queue, (new_dist, neighbor))

        for node in self.G.nodes():
            if distances[node] == float("inf"):
                continue
            path = self._restore_path(parent, node)
            self.previsit(node, path=path)
        
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

