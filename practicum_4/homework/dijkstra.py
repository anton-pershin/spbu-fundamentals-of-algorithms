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
        G=self.G
        INF = float("inf")
        dist = {v: INF for v in G.nodes}
        prev = {v: None for v in G.nodes}
        dist[node] = 0
        pq = []
        heapq.heappush(pq, (0, node))
        while pq:
            c_dist, nearest = heapq.heappop(pq)
            if c_dist != dist[nearest]:
                continue

            for t,a in G[nearest].items():
                w = a["weight"]
                if dist[t] > dist[nearest] + w:
                    dist[t] = dist[nearest] + w
                    prev[t] = nearest
                    heapq.heappush(pq, (dist[t], t))
        self.shortest_paths = {}
        for target in G.nodes:
            path = []
            cur  = target
            while cur is not None:
                path.append(cur)
                cur = prev[cur]
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

