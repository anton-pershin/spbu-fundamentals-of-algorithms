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

    def run(self, start_node: Any) -> None:
        if start_node not in self.graph:
            raise ValueError(f"Узел {start_node!r} отсутствует в графе.")

        self.visited: set[Any] = set()
        nodes_queue: deque[Any] = deque()

        self.visited.add(start_node)
        self.previsit(start_node)
        nodes_queue.append(start_node)

        while nodes_queue:
            node = nodes_queue.popleft()

            for adj in self.graph.neighbors(node):
                if adj not in self.visited:
                    self.visited.add(adj)
                    self.previsit(adj)
                    nodes_queue.append(adj)

            self.postvisit(node)
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
    dfs.run("0")
    print()

    plot_graph(G)