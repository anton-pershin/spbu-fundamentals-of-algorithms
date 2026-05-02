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
        self.mst_edges = []
        self.total_weight = 0

    def run(self, node: Any) -> None:
        S = {node}
        queue = []

        for neighbor in self.G.neighbors(node):
            weight = self.G[node][neighbor]['weight']
            heapq.heappush(queue, (weight, node, neighbor))

        while len(S) < self.G.number_of_nodes() and queue:
            weight, u, v = heapq.heappop(queue)
            if v in S:
                continue

            self.mst_edges.append((u, v))
            self.total_weight += weight
            S.add(v)
            for neighbor in self.G.neighbors(v):
                if neighbor not in S:
                    new_weight = self.G[v][neighbor]['weight']
                    heapq.heappush(queue, (new_weight, v, neighbor))

if __name__ == "__main__":
    G = nx.read_edgelist(
        Path("..") / "practicum_4" / "simple_weighted_graph_9_nodes.edgelist",
        create_using=nx.Graph
    )
    plot_graph(G)

    prim = PrimAlgorithm(G)
    mst_edges = prim.run(node="0")

    plot_graph(G, highlighted_edges=list(prim.mst_edges))

