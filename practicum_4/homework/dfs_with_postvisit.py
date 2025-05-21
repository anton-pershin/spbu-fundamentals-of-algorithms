from pathlib import Path
from collections import deque
from typing import Any
from abc import ABC, abstractmethod

import networkx as nx
from networkx.classes import neighbors

from practicum_4.dfs import GraphTraversal
from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class DfsViaLifoQueueWithPostvisit(GraphTraversal):
    def run(self, node: Any) -> None:
        visited = set()
        stack = deque()

        stack.append((node, False))

        while stack:
            cur_node, processed = stack.pop()

            if processed:
                self.postvisit(cur_node)
                continue

            if cur_node in visited:
                continue

            visited.add(cur_node)
            self.previsit(cur_node)

            stack.append((cur_node, True))

            neighbors = sorted(self.G.neighbors(cur_node), reverse=True)
            for neigh in neighbors:
                if neigh not in visited:
                    stack.append((neigh, False))


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

