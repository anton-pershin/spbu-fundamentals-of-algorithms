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
        visited = {}
        for v in self.G:
            visited[v] = 0
        
        stack = [node]
        while len(stack) > 0:
            v = stack.pop()
            if visited[v] == 0:
                self.previsit(v)
                visited[v] = 1
                stack.append(v)

                for u in reversed(list(self.G.neighbors(v))):
                    if visited[u] == 0:
                        stack.append(u)

            elif visited[v] == 1:
                self.postvisit(v)
                visited[v] = 2


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
    # plot_graph(G)

    dfs = DfsViaLifoQueueWithPrinting(G)
    dfs.run(node="0")