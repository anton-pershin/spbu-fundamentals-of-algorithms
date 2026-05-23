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

        distances = {v: float('inf') for v in self.G.nodes()}
        distances[node] = 0
        parent_map = {v: None for v in self.G.nodes()}

        queue = [(0, node)]

        while queue:
            cur_dist, u = heapq.heappop(queue)

            if cur_dist > distances[u]:
                continue

            for v in self.G.neighbors(u):
                weight = float(self.G[u][v].get('weight', 1))
                new_dist = cur_dist + weight

                if new_dist < distances[v]:
                    distances[v] = new_dist
                    parent_map[v] = u
                    heapq.heappush(queue, (new_dist, v))

        for target in self.G.nodes():
            if distances[target] == float('inf'):
                continue

            path = []
            curr = target
            while curr is not None:
                path.append(curr)
                curr = parent_map[curr]
            path.reverse()

            self.previsit(target, path=path)

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

