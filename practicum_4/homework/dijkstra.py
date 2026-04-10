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
        distances = {node: float("inf") for node in self.G.nodes()}
        distances[node] = 0
        priority_queue = [(0, node)]
        paths = {node: [node]} 

        while priority_queue:
            min_index = 0 
            for i in range(len(priority_queue)):
                if priority_queue[i][0] < priority_queue[min_index][0]:
                    min_index = i

            current_distance, current_node = priority_queue.pop(min_index) 
            if current_node in self.visited:
                continue

            self.visited.add(current_node)
            self.previsit(current_node, path=paths[current_node])

            for neighbor in self.G.neighbors(current_node): 
                if neighbor not in self.visited:
                    edge_weight = self.G[current_node][neighbor].get("weight", 1) 
                    updated_distance = current_distance + edge_weight 

                    if updated_distance < distances[neighbor]:
                        distances[neighbor] = updated_distance
                        paths[neighbor] = paths[current_node] + [neighbor]
                        priority_queue.append((updated_distance, neighbor))

            self.postvisit(current_node )


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