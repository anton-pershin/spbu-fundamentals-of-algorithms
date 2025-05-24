from pathlib import Path
from collections import deque
from typing import Any
from abc import ABC, abstractmethod

import networkx as nx

from practicum_4.dfs import GraphTraversal
from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class DfsViaLifoQueueWithPostvisit(GraphTraversal):
    def previsit(self, node: Any, **params) -> None:
        print(f"Previsit {node}")
    def postvisit(self, node: Any, **params) -> None:
        print(f"Postvisit {node}")
    def run(self, node: Any) -> None:
        stack = [node]
        visited_postvisit = set()

        while len(stack) > 0:
            node = stack[-1]

            if node not in self.visited:
                self.previsit(node)
                self.visited.add(node)

                for n_neigh in self.G.neighbors(node):
                    if n_neigh not in self.visited:
                        stack.append(n_neigh)
            else:
                if node not in visited_postvisit:
                    self.postvisit(node)
                    visited_postvisit.add(node)
                stack.pop()


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

