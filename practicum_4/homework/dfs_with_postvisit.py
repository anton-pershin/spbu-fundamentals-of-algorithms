
import sys
import os

# (чтобы можно было импортировать из src)
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

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
        stack = deque([node])
        visited = set()
        route = []

        while len(stack) > 0:
            current_node = stack.pop()
            if current_node not in visited:
                visited.add(current_node)
                self.previsit(current_node)
                for neighbor in self.G.neighbors(current_node):
                    if neighbor not in visited:
                        stack.append(neighbor)
                self.postvisit(current_node)
                route.append(current_node)
        print("-" * 20, "\n", "Complete route taken: ", " -> ".join(route))


class DfsViaLifoQueueWithPrinting(DfsViaLifoQueueWithPostvisit):
    def previsit(self, node: Any, **params) -> None:
        print(f"Previsit node {node}")

    def postvisit(self, node: Any, **params) -> None:
        print(f"Postvisit node {node}")



if __name__ == "__main__":
    G = nx.read_edgelist(
        Path("practicum_4") / "simple_graph_10_nodes.edgelist",
        create_using=nx.Graph
    )

    dfs = DfsViaLifoQueueWithPrinting(G)
    dfs.run(node="0")

    plot_graph(G)


