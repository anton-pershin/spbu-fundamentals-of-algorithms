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
        d = {n: float('inf') for n in self.G.nodes}
        d[node] = 0
        q = [(0, node, [node])]
        seen = set()

        while q:
            dist_u, u, path_u = heapq.heappop(q)
            
            if u in seen:
                continue
            
            seen.add(u)
            self.previsit(u, path=path_u)

            for v in self.G.neighbors(u):
                edge = self.G.get_edge_data(u, v)
                w = edge.get('weight', 1)
                new_d = dist_u + w
                
                if new_d < d[v]:
                    d[v] = new_d
                    heapq.heappush(q, (new_d, v, path_u + [v]))


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

