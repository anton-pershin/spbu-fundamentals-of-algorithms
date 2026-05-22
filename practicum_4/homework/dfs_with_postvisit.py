from pathlib import Path
from collections import deque
from typing import Any
from abc import ABC, abstractmethod

import networkx as nx

from practicum_4.dfs import GraphTraversal
from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class DfsViaLifoQueueWithPostvisit(GraphTraversal):
    def run(self, node: Any) -> None:
        inDepth = deque()
        outDepth = deque()
        inDepth.append(node)
        
        while len(inDepth) != 0:
            current = inDepth.pop()
            hasUntouchedNeighbors = False
            
            self.previsit(current)
            self.visited.add(current)
            
            for neighbor in G.neighbors(current):
                if neighbor not in self.visited:
                    # If there is a cycle, it won't let us fall in it
                    if neighbor not in inDepth:
                        inDepth.append(neighbor)
                    hasUntouchedNeighbors = True

            if hasUntouchedNeighbors != False:
                # Leave "bread crumbs"
                outDepth.append(current)
            else:
                self.postvisit(current)
        
        # Return by "bread crumbs"
        while len(outDepth) != 0:
            self.postvisit(outDepth.pop())

class DfsViaLifoQueueWithPrinting(DfsViaLifoQueueWithPostvisit):
    def previsit(self, node: Any, **params) -> None:
        print(f"Previsit node {node}")

    def postvisit(self, node: Any, **params) -> None:
        print(f"Postvisit node {node}")


if __name__ == "__main__":
    # Load and plot the graph
    G = nx.read_edgelist(
        Path("practicum_4") / "simple_graph_10_nodes.edgelist",
        create_using=nx.Graph
    )
    plot_graph(G)

    dfs = DfsViaLifoQueueWithPrinting(G)
    dfs.run(node="0")

