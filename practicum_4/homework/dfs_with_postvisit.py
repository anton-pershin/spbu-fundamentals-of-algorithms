from pathlib import Path
from collections import deque
from typing import Any
from abc import ABC, abstractmethod
from pathlib import Path

import sys
sys.path.append(r"/Users/alexanderkuka/documents/python/pershin/spbu-fundamentals-of-algorithms")
import networkx as nx

from practicum_4.dfs import GraphTraversal
from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph



class DfsViaLifoQueueWithPostvisit(GraphTraversal):
    def run(self, node: Any) -> None:

        stack = [(node, False)]

        while len(stack) > 0:
            node, status = stack.pop()

            if status:
                self.postvisit(node)
                print(stack)
                continue

            if node not in self.visited:
                self.visited.add(node)
                self.previsit(node)
                stack.append((node, True))
                print(stack)

                for n_neigh in self.G.neighbors(node):
                    if n_neigh not in self.visited:
                        stack.append((n_neigh, False))
                        # print(stack)
            # print(stack)
            # print(self.visited)



        pass


class DfsViaLifoQueueWithPrinting(DfsViaLifoQueueWithPostvisit):
    def previsit(self, node: Any, **params) -> None:
        self.visited.add(node)
        print(f"Previsit node {node}")

    def postvisit(self, node: Any, **params) -> None:
        
        print(f"Postvisit node {node}")


if __name__ == "__main__":
    # Load and plot the graph
    G = nx.read_edgelist("pershin/spbu-fundamentals-of-algorithms/practicum_4/simple_graph_10_nodes.edgelist")
    # plot_graph(G)

    dfs = DfsViaLifoQueueWithPrinting(G)
    dfs.run(node="0")

