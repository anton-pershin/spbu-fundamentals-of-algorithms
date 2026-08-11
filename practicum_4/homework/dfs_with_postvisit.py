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
        stack = [(node, iter(self.G.neighbors(node)), False)]
        visited = set()

        while stack:
            cur, neighbors, is_postvisit = stack.pop()
            if is_postvisit:
                self.postvisit(cur)
                continue
            if cur in visited:
                continue

            visited.add(cur)
            self.previsit(cur)
            stack.append((cur, None, True))

            neighbors_list = list(self.G.neighbors(cur))
            for neighbor in reversed(neighbors_list):
                if neighbor not in visited:
                    stack.append((neighbor, iter(self.G.neighbors(neighbor)), False))


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

