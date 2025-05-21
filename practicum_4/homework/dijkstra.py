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
        super().__init__(G)

    def previsit(self, node: Any, **params) -> None:
        """List of params:
        * path: list[Any] (path from the initial node to the given node)
        """
        self.shortest_paths[node] = params["path"]

    def postvisit(self, node: Any, **params) -> None:
        pass

    def run(self, node: Any) -> None:
        dist: dict[Any, float] = {n: float('inf') for n in self.G.nodes()}
        dist[node] = 0.0

        self.shortest_paths = {}
        self.previsit(node, path=[node])

        unvisited = set(self.G.nodes())

        while unvisited:
            u = min(unvisited, key=lambda v: dist[v])
            if dist[u] == float('inf'):
                break

            unvisited.remove(u)

            for v, data in self.G[u].items():
                if v in unvisited:
                    weight = data.get('weight', 1.0)
                    alt = dist[u] + weight
                    if alt < dist[v]:
                        dist[v] = alt
                        new_path = self.shortest_paths[u] + [v]
                        self.previsit(v, path=new_path)


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

