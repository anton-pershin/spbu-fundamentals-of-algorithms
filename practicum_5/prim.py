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
        self.G : AnyNxGraph = G
        self.mst_edges = set()
        self.visited = set()

    def run(self, node: Any) -> None:
        heap = [(0,node,None)]
        while heap:
            weight,curNode, parent = heapq.heappop(heap)
    
            if curNode in self.visited:
                continue

            self.visited.add(curNode)

            if parent is not None:
                self.mst_edges.add((curNode,parent))

            for adj in self.G[curNode]:
                if adj not in self.visited:
                    heapq.heappush(heap,(self.G[curNode][adj]["weight"],adj,curNode))

                
if __name__ == "__main__":
    G = nx.read_edgelist(
        Path("practicum_4") / "simple_weighted_graph_9_nodes.edgelist",
        create_using=nx.Graph
    )
    plot_graph(G)

    prim = PrimAlgorithm(G)
    mst_edges = prim.run(node="0")

    plot_graph(G, highlighted_edges=list(prim.mst_edges))

