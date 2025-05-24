from pathlib import Path
from queue import PriorityQueue
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
        self.shortest_paths[node] = params["path"]

    def postvisit(self, node: Any, **params) -> None:
        pass

    def run(self, node: Any) -> None:  
        distances = {vertex: float('inf') for vertex in self.G.nodes}
        distances[node] = 0
        priority_queue = [(0, node, [node])]
        processed = set()

        while priority_queue:
            dist_u, u, curr_path = heapq.heappop(priority_queue)
            if u in processed:
                continue
            processed.add(u)
            self.previsit(u, path=curr_path)
            for v in self.G.neighbors(u):
                attributes = self.G.get_edge_data(u, v)
                w = attributes.get('weight', 1)
                cand_dist = dist_u + w
                if cand_dist < distances[v]:
                    distances[v] = cand_dist
                    heapq.heappush(priority_queue, (cand_dist, v, curr_path + [v]))


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
