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
        self.G = G
        self.nodes = set()
        self.mst_edges = set()

    def run(self, node: Any) -> None:
        self.nodes.add(node)
        data = []
        counter = 0

        for edge in self.G.edges(node, data=True):
            if (edge[0] not in self.nodes) or (edge[1] not in self.nodes):
                counter += 1
                heapq.heappush(data, (edge[2]['weight'], (counter, edge[0], edge[1])))
                
        while len(self.nodes) != len(self.G):
            length, (k, first_node, second_node) = heapq.heappop(data)

            if (first_node not in self.nodes) or (second_node not in self.nodes):
                self.mst_edges.add((first_node, second_node))

            current_node = first_node if first_node not in self.nodes else second_node
            self.nodes.add(current_node)

            for edge in self.G.edges(current_node, data=True):
                if ((edge[0] not in self.nodes) or (edge[1] not in self.nodes)):
                    counter += 1
                    heapq.heappush(data, (edge[2]['weight'], (counter, edge[0], edge[1])))

if __name__ == "__main__":
    G = nx.read_edgelist(
        Path("practicum_4") / "simple_weighted_graph_9_nodes.edgelist",
        create_using=nx.Graph
    )
    plot_graph(G)

    prim = PrimAlgorithm(G)
    prim.run(node="0")

    plot_graph(G, highlighted_edges=list(prim.mst_edges))

