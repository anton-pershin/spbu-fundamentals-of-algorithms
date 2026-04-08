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
        queue = deque()
        self.visited.add(node)
        queue.append(node)
        
        while len(queue) > 0:
            current = queue.popleft()
            self.previsit(current)
            
            for neigh in self.G.neighbors(current):
                if neigh not in self.visited:
                    self.visited.add(neigh)
                    queue.append(neigh)
            
            self.postvisit(current)

class BfsViaLifoQueueWithPrinting(BfsViaFifoQueue):
    def previsit(self, node: Any, **params) -> None:
        print(f"Previsit node {node}")

    def postvisit(self, node: Any, **params) -> None:
        print(f"Postvisit node {node}")


if __name__ == "__main__":
    G = nx.read_edgelist(
        Path("practicum_4") / "simple_graph_10_nodes.edgelist",
        create_using=nx.Graph
    )


    print("Iterative BFS")
    print("-" * 32)
    bfs = BfsViaLifoQueueWithPrinting(G)
    bfs.run(node="0")
    print()

    plot_graph(G)