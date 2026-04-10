from pathlib import Path
from collections import deque
from typing import Any
from abc import ABC, abstractmethod
from collections import deque

import networkx as nx

from practicum_4.dfs import GraphTraversal, DfsViaRecursion
from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class BfsViaFifoQueue(GraphTraversal):
    def run(self, node: Any) -> None:
        queue = deque()
        queue.append(node)
        self.visited = set()
        self.visited.add(node)

        while queue:
            neighbors = self.G.neighbors(queue[0])
            for neighbor in neighbors:
                if neighbor not in self.visited:
                    self.previsit(neighbor)
                    self.visited.add(neighbor)
                    queue.append(neighbor)

            self.postvisit(queue.popleft())



class BfsViaLifoQueueWithPrinting(DfsViaRecursion):
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

    # Iterative BFS. Makes use of FIFO data structure
    print("Iterative BFS")
    print("-" * 32)
    dfs = BfsViaLifoQueueWithPrinting(G)
    dfs.run(node="0")
    print()

    plot_graph(G)

