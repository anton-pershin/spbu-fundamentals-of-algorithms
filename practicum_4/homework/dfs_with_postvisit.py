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

        stack = deque()
        stack.append([node, False])
        arr = list()

        while len(stack) > 0:

            new_node, flag = stack.pop()
            if flag:
                self.postvisit(new_node)
                continue
            if new_node not in self.visited:
                self.visited.add(new_node)
                self.previsit(new_node)
                stack.append([new_node, True])

                for n_neigh in sorted(self.G.neighbors(new_node), reverse=True):
                    if n_neigh not in self.visited:
                        stack.append([n_neigh, False])


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
