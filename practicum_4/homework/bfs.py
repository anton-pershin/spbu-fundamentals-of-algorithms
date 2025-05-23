from pathlib import Path
from collections import deque
from typing import Any
from abc import ABC, abstractmethod
import sys
sys.path.append(r"/home/viktoria/algoritms/spbu-fundamentals-of-algorithms")

import networkx as nx

from practicum_4.homework.dfs import GraphTraversal 
from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


from collections import deque
from typing import Any

class BfsViaFifoQueue(GraphTraversal):
    def __init__(self, graph: AnyNxGraph):
        self.graph = graph 

    def run(self, node: Any) -> None:
        if not node in self.graph:
            raise ValueError("node not found")

        self.visited = set()
        
        queue = deque()
        self.visited.add(node)
        self.previsit(node)
        queue.append(node)

        while len(queue) != 0:
            current = queue.popleft()
            
            for neighbour in self.graph.neighbors(current):
                if not neighbour in self.visited:
                    self.visited.add(neighbour)
                    self.previsit(neighbour)
                    queue.append(neighbour)
            
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
    dfs = BfsViaLifoQueueWithPrinting(G)
    dfs.run(node="0")
    print()

    plot_graph(G)

