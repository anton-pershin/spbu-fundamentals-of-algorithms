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

        visited = set()
        visited.add(node)
        
        lifo_queue = deque()
        lifo_queue.append((node, "previsit"))

        while lifo_queue:
            current, state = lifo_queue.pop()

            if state == "postvisit":
                self.postvisit(current)
                continue

            self.previsit(current)
            lifo_queue.append((current, "postvisit"))
            
            for child_node in self.G.neighbors(current):
                if child_node not in visited:
                    visited.add(child_node)
                    lifo_queue.append((child_node, "previsit"))
                
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
    # plot_graph(G)

    dfs = DfsViaLifoQueueWithPrinting(G)
    dfs.run(node="0")

