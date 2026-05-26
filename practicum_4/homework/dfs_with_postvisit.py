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
        stack = [(node, iter(self.G.neighbors(node)))]
        
        self.previsit(node)
        self.visited.add(node)
        
        while stack:
            current_node, neighbors_iter = stack[-1]
            
            try:
                neighbor = next(neighbors_iter)
                
                if neighbor not in self.visited:
                    self.previsit(neighbor)
                    self.visited.add(neighbor)
                    stack.append((neighbor, iter(self.G.neighbors(neighbor))))
            except StopIteration:
                stack.pop()
                self.postvisit(current_node)


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