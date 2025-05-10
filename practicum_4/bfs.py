from pathlib import Path
from collections import deque
from typing import Any
from abc import ABC, abstractmethod

import networkx as nx

from practicum_4.dfs import GraphTraversal 
from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class BfsViaFifoQueue(GraphTraversal):
    def __init__(self, graph: AnyNxGraph):
        self.graph = graph

    def run(self, node: Any) -> None:
        """
        Iterative breadth-first search starting at `node`.
        Nodes are discovered level by level by means of a FIFO queue.
        """

        # Safety check – start node must exist
        if node not in self.graph:
            raise ValueError(f"Start node {node!r} is not contained in the graph.")

        # Reset/initialise bookkeeping
        self.visited: set[Any] = set()

        # FIFO queue (left = pop side, right = push side)
        queue: deque[Any] = deque()

        # Discover the start node
        self.visited.add(node)
        self.previsit(node)
        queue.append(node)

        # Main loop
        while queue:
            current = queue.popleft()

            # Explore all undiscovered neighbours
            for neighbour in self.graph.neighbors(current):
                if neighbour not in self.visited:
                    self.visited.add(neighbour)
                    self.previsit(neighbour)
                    queue.append(neighbour)

            # All neighbours processed → finish current node
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

