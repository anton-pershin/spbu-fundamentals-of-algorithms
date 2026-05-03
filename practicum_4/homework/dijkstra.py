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
        dist = {n: float('inf') for n in self.G.nodes()}
        dist[node] = 0
        path = {n: None for n in self.G.nodes()}
        priority_queue = [(0, node)]

        while priority_queue:
            distance, name = heapq.heappop(priority_queue)
            if distance > dist[name]:
                continue

            for neighbor in self.G.neighbors(name):
                weight = self.G[name][neighbor].get('weight', 1)
                new_d = distance + weight

                if new_d < dist[neighbor]:
                    dist[neighbor] = new_d
                    path[neighbor] = name
                    heapq.heappush(priority_queue, (new_d, neighbor))
        
        for n in self.G.nodes():
            if dist[n] == float('inf'):
                continue
            final_path = []
            current = n
            while current is not None:
                final_path.append(current)
                current = path[current]
            final_path.reverse()
            self.previsit(n, path=final_path)


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

