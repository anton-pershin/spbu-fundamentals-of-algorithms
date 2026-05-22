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
        
        stack = deque()
        stack.append((node, False))
        
        while stack:
            current_node, is_postvisit_phase = stack.pop()
            
            if is_postvisit_phase:
                self.postvisit(current_node)
            else:
                if current_node not in self.visited:
                    self.visited.add(current_node)
                    self.previsit(current_node)
                    
                    stack.append((current_node, True))
                    
                    neighbors = list(self.G.neighbors(current_node))
                    for neighbor in reversed(neighbors):
                        if neighbor not in self.visited:
                            stack.append((neighbor, False))


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
    # plot_graph(G)