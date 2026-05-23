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

        stack = deque([(node, "ENTER")])
        visited = {node}

        while stack:
            u, action = stack.pop()

            if action == "EXIT":
                self.postvisit(u)
            
            elif action == "ENTER":
                self.previsit(u)
                
                stack.append((u, "EXIT"))
                
                for v in reversed(list(self.G.neighbors(u))):
                    if v not in visited:
                        visited.add(v)
                        stack.append((v, "ENTER"))

        pass


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

