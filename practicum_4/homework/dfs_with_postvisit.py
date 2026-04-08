from abc import ABC, abstractmethod
from pathlib import Path
from collections import deque
from typing import Any

import networkx as nx

from practicum_4.dfs import GraphTraversal
from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph

class DfsViaLifoQueueWithPostvisit(GraphTraversal):
    def run(self, node: Any) -> None:
        visited = set()
        queue = deque()
        queue.append((node, "previsit"))
        
        while queue:
            current, phase = queue.pop()
            if phase == "postvisit":
                self.postvisit(current)
                continue
                
            if current in visited:
                continue
            
            self.previsit(current)
            visited.add(current)
            queue.append((current, "postvisit"))
            
            for child in self.G.neighbors(current):
                if child not in visited:
                    queue.append((child, "previsit"))
                 
                 
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

