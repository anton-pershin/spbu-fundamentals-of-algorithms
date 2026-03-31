from pathlib import Path
from typing import Any
from abc import ABC, abstractmethod
from collections import deque

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

    def _closest(self, distances : dict, visited : set) -> Any:
        best_node = None
        best_dist = float('inf')

        for node in self.G.nodes:
            if node not in visited and distances[node] < best_dist:
                best_dist = distances[node]
                best_node = node

        return best_node

    def _build_path(self, previous : dict, start : Any, end : Any) -> list:
        path = []
        cur = end
        while cur is not None:
            path.append(cur)
            cur = previous[cur]
        path.reverse()
        return path

    def run(self, node: Any) -> None:
        distances = {v: float('inf') for v in self.G.nodes}
        distances[node] = 0
        visited = set()
        previous = {v : None for v in self.G.nodes}
        while len(visited) < len(self.G.nodes):
            cur = self._closest(distances,visited)
            
            if cur == None:
                break

            visited.add(cur)

            for adj in self.G.neighbors(cur):
                if (adj in visited):
                    continue

                weight = self.G[cur][adj].get("weight",1)
                newDist = distances[cur] + weight

                if newDist < distances[adj]:
                    distances[adj] = newDist
                    previous[adj] = cur
        for n in self.G.nodes:
            self.shortest_paths[n] = self._build_path(previous,node,n)



if __name__ == "__main__":
    G = nx.read_edgelist(
        Path("practicum_4") / "simple_weighted_graph_9_nodes.edgelist",
        create_using=nx.Graph
    )
    plot_graph(G)

    sp = DijkstraAlgorithm(G)
    sp.run("0")

    test_node = "5"
    print(sp.shortest_paths[test_node])
    shortest_path_edges = [
        (sp.shortest_paths[test_node][i], sp.shortest_paths[test_node][i + 1])
        for i in range(len(sp.shortest_paths[test_node]) - 1)
    ]
    plot_graph(G, highlighted_edges=shortest_path_edges)

