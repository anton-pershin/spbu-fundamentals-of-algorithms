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
        dist = {n: float('inf') for n in self.G.nodes}
        dist[node] = 0
        self.shortest_paths[node] = [node]

        heap = []
        heapq.heappush(heap, (0, node))

        while heap:
            cur_dist, cur_node = heapq.heappop(heap)

            if cur_dist > dist[cur_node]:
                continue

            for neigh in self.G.neighbors(cur_node):
                weight = self.G[cur_node][neigh].get('weight', 1)
                new_dist = cur_dist + weight

                if new_dist < dist[neigh]:
                    dist[neigh] = new_dist
                    self.shortest_paths[neigh] = self.shortest_paths[cur_node] + [neigh]
                    heapq.heappush(heap, (new_dist, neigh))


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

