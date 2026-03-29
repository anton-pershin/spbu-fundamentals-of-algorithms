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
        result = {node: float('inf') for node in self.G.nodes()}
        paths = {node: [] for node in self.G.nodes()}

        queue = []
        heapq.heappush(queue, (0, [0, node, ['0']]))
        counter = 0
        
        while queue:
            counter += 1
            dist, data = heapq.heappop(queue)
            node, path = data[1], data[2]
            self.visited.add(node)

            if dist < result[node]:
                result[node] = dist
                paths[node] = path

            for neighbor in self.G.neighbors(node):
                counter += 1

                if neighbor not in self.visited:
                    heapq.heappush(queue, (dist + self.G[node][neighbor]['weight'], [counter, neighbor, path + [neighbor]]))

        self.shortest_paths = paths

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



