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

        postvisit_deque = deque()
        stack = [node]

        while len(stack) > 0:
            node = stack.pop()
            if node not in self.visited:
                self.previsit(node)
                self.visited.add(node)
                postvisit_deque.append(node)
                for i in self.G.neighbors(node):
                    if i not in self.visited:
                        stack.append(i)

        while len(postvisit_deque) > 0:
            node = postvisit_deque.pop()
            self.postvisit(node)


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

