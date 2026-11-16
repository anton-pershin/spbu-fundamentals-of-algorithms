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
        self.shortest_paths[node] = params["path"]

    def postvisit(self, node: Any, **params) -> None:
        pass

    def run(self, node: Any) -> None:

        import heapq

        dist = {node: 0.0}
        paths = {node: [node]}
        pq = [(0.0, 0, node)]
        counter = 1
        while pq:
            d, _, u = heapq.heappop(pq)
            if u in self.visited:
                continue
            self.visited.add(u)
            self.previsit(u, path=paths[u])
            for v in self.G.neighbors(u):
                if v in self.visited:
                    continue
                new_d = d + self.G[u][v].get("weight", 1)
                if v not in dist or new_d < dist[v]:
                    dist[v] = new_d
                    paths[v] = paths[u] + [v]
                    heapq.heappush(pq, (new_d, counter, v))
                    counter += 1
            self.postvisit(u)


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

