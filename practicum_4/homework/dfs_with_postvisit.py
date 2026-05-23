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
        stack = []
        self.previsit(node)
        stack.append(node)
        self.visited.add(node)
        
        while stack:
            cur_node = stack[-1]

            if cur_node not in self.visited:
                self.previsit(cur_node)
                self.visited.add(cur_node)
                
            for neighbor in G.neighbors(cur_node):
                if neighbor not in self.visited:
                    stack.append(neighbor)
                    break
            else:
                self.postvisit(stack.pop())
    



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
