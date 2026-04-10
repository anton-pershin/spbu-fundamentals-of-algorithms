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
            n, state = stack.pop()

            if not state:
                if n in self.visited:
                    continue
                stack.append((n, True))
                self.previsit(n)
                self.visited.add(n)
                for i in reversed(list(self.G.neighbors(n))):
                    if not i in self.visited:
                        stack.append((i, False))
            
            else:
                self.postvisit(n)


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
    

    dfs = DfsViaLifoQueueWithPrinting(G)
    dfs.run(node="0")

    plot_graph(G)

