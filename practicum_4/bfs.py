from pathlib import Path
from collections import deque
from typing import Any
from abc import ABC, abstractmethod

import networkx as nx

from practicum_4.dfs import GraphTraversal 
from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class BfsViaFifoQueue(GraphTraversal):
    def run(self, node: Any) -> None:

        self.reset()  # очистить visited перед запуском
        queue = deque([node])

        while queue:
            current = queue.popleft()

            if current not in self.visited:
                self.visited.add(current)
                self.previsit(current)

                for neighbor in self.G.neighbors(current):
                    if neighbor not in self.visited:
                        queue.append(neighbor)

                self.postvisit(current)



class BfsViaLifoQueueWithPrinting(BfsViaFifoQueue):
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

