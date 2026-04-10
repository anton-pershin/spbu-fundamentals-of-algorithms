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
        dist = {}
        for v in self.G.nodes():
            dist[v] = float("inf")
        dist[node] = 0
        prev = {}
        for v in self.G.nodes():
            prev[v] = None

        pq = [(0, node)]

        while len(pq) > 0:
            d, v = heapq.heappop(pq)
            if d > dist[v]:
                continue
            path = []
            cur = v
            while cur is not None:
                path.append(cur)
                cur = prev[cur]
            path.reverse()

            self.previsit(v, path=path)

            for u in self.G.neighbors(v):
                w = self.G[v][u]["weight"]
                if dist[v] + w < dist[u]:
                    dist[u] = dist[v] + w
                    prev[u] = v
                    heapq.heappush(pq, (dist[u], u))


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