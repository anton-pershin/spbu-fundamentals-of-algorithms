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
        self.visited = set()
        stack = [(node, False)]  # (node, postvisit_flag)

        while stack:
            node, post = stack.pop()
            if post:
                # Поствизит
                self.postvisit(node)
            else:
                if node not in self.visited:
                    # Предвизит
                    self.previsit(node)
                    self.visited.add(node)
                    # Запланировать поствизит после обхода соседей
                    stack.append((node, True))
                    # Добавляем соседей для предвизита
                    for nbr in reversed(list(self.G.neighbors(node))):
                        if nbr not in self.visited:
                            stack.append((nbr, False))

                    

            

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

