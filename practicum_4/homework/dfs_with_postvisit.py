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
        ENTER, EXIT = 0, 1
        stack = deque()
        stack.append((node, ENTER))

        while stack:
            current_node, state = stack.pop()

            if state == EXIT:
                self.postvisit(current_node)

            elif state == ENTER:
                if current_node in self.visited:
                    continue

                self.visited.add(current_node)
                self.previsit(current_node)
                stack.append((current_node, EXIT))

                for neighbor in self.G.neighbors(current_node):
                    if neighbor not in self.visited:
                        stack.append((neighbor, ENTER))


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

