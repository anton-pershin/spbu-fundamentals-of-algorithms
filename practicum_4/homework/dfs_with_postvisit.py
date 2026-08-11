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
        stack = [(node, False)]
        
        while stack:
            current, processed = stack.pop()
            
            if not processed:
                if current in self.visited:
                    continue
                
                self.previsit(current)
                self.visited.add(current)
                
                stack.append((current, True))
                
                for neighbor in reversed(list(self.G.neighbors(current))):
                    if neighbor not in self.visited:
                        stack.append((neighbor, False))
            else:

                self.postvisit(current)


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
    #plot_graph(G)

    dfs = DfsViaLifoQueueWithPrinting(G)
    dfs.run(node="0")