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

        visited = set()
        stack = [(node, False)]

        pass
        while stack:
            current, processed = stack.pop()

            if current in visited and not processed:
                continue

            if processed:
                self.postvisit(current)
                continue

            visited.add(current)
            self.previsit(current)

            stack.append((current, True))

            for neighbor in reversed(list(self.G.neighbors(current))):
                if neighbor not in visited:
                    stack.append((neighbor, False))
                    


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