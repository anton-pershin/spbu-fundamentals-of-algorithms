from pathlib import Path
import heapq
from typing import Any
from abc import ABC, abstractmethod


import networkx as nx
import numpy as np

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class PrimAlgorithm:
    def __init__(self, G: AnyNxGraph) -> None:

        self.G: AnyNxGraph = G
        self.mst_set: set[Any] = set()
        self.rest_set: set[Any] = set(G.nodes())
        self.mst_edges: set[tuple[Any, Any]] = set()

    def run(self, node: Any) -> None:
        node_to_add = node
        edge = None
        priority_queue = []

        while self.rest_set:
            if node_to_add not in self.mst_set:
                if edge is not None:
                    self.mst_edges.add(edge)
                
                self.mst_set.add(node_to_add)
                self.rest_set.add(node_to_add)
            
            for n_start, n_end, data in self.G.edges(node_to_add, data=True):
                heapq.heappush(priority_queue, (data["weight"], (n_start, n_end,)))

            _, edge = heapq.heappop(priority_queue)
            node_to_add = edge[1]


            
        


if __name__ == "__main__":
    G = nx.read_edgelist(
        Path("practicum_4") / "simple_weighted_graph_9_nodes.edgelist",
        create_using=nx.Graph
    )
    plot_graph(G)

    prim = PrimAlgorithm(G)
    mst_edges = prim.run(node="0")

    plot_graph(G, highlighted_edges=list(prim.mst_edges))

