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

    def run(self, node: Any) -> None:
        dist = {n: float('inf') for n in self.G.nodes}
        dist[node] = 0
        heap = [(0, node, [node])]
        visited = set()

        while heap:
            curr_dist, curr_node, path = heapq.heappop(heap)
            if curr_node in visited:
                continue
            visited.add(curr_node)
            self.previsit(curr_node, path=path)
            for neighbor in self.G.neighbors(curr_node):
                edge_attr = self.G.get_edge_data(curr_node, neighbor)
                weight = edge_attr.get('weight', 1)
                new_dist = curr_dist + weight
                if new_dist < dist[neighbor]:
                    dist[neighbor] = new_dist
                    heapq.heappush(heap, (new_dist, neighbor, path + [neighbor]))


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

