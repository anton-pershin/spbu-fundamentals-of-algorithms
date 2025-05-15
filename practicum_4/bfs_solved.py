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
        queue = deque()  # (node, processed_flag), processed is for postvisit
        self.visited.add(node)
        self.previsit(node)
        queue.appendleft((node, False))

        while len(queue) > 0:
            node, processed = queue.pop()
            
            # neighbors == successors in DiGraph
            for n_neigh in self.G.neighbors(node):
                if n_neigh not in self.visited:
                    self.visited.add(n_neigh)
                    self.previsit(n_neigh)
                    queue.appendleft((n_neigh, False))

            self.postvisit(node)


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

