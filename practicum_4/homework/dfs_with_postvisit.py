from pathlib import Path
from collections import deque
from typing import Any
from abc import ABC, abstractmethod

import networkx as nx

from practicum_4.dfs import GraphTraversal
from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class DfsViaLifoQueueWithPostvisit(GraphTraversal):
    def __init__(self, graph):
        self.graph = graph
    def run(self, node: Any) -> None:
        visited = set()
        stack = deque()
        # (node, state): state == 'enter' or 'exit'
        stack.append((node, 'enter'))
        while stack:
            current, state = stack.pop()
            if state == 'enter':
                if current in visited:
                    continue
                # Previsit logic
                self.previsit(current)
                visited.add(current)
                # Prepare for postprocessing
                stack.append((current, 'exit'))
                # Add neighbors to stack
                for neighbor in reversed(list(self.graph.neighbors(current))):
                    if neighbor not in visited:
                        stack.append((neighbor, 'enter'))
            elif state == 'exit':
                # Postvisit logic
                self.postvisit(current)


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
    plot_graph(G)

    dfs = DfsViaLifoQueueWithPrinting(G)
    dfs.run(node="0")

