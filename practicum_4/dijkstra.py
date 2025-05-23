from pathlib import Path
from queue import PriorityQueue
import heapq
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
        self.dist = {nd: float("inf") for nd in G.nodes()}
        self.dist[node] = 0
        self.shortest_paths[node] = [node]
        priorQue = [(0, node)]
        
        while len(priorQue) > 0:
            curr_dist, curr_node = heapq.heappop(priorQue)
            if curr_node in self.visited:
                continue
            self.visited.add(curr_node)
            
            for n_neigh in self.G.neighbors(curr_node):
                weight = self.G[curr_node][n_neigh].get('weight', 1)
                
                dist = curr_dist + weight
                
                if dist < self.dist[n_neigh]:
                    self.dist[n_neigh] = dist
                    self.shortest_paths[n_neigh] = self.shortest_paths[curr_node] + [n_neigh]
                    heapq.heappush(priorQue, (dist, n_neigh))


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

