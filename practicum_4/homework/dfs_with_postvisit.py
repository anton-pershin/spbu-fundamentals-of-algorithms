
import sys
import os

# (чтобы можно было импортировать из src)
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

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
        stack = deque([(node, False)])
        visited = set()

        while len(stack) > 0:
            current_node, processed = stack.pop()
            if processed:
                self.postvisit(current_node)
                continue
                
            if current_node not in visited:
                visited.add(current_node)
                self.previsit(current_node)
                stack.append((current_node, True))
                for neighbor in list(self.G.neighbors(current_node))[::-1]:
                    if neighbor not in visited:
                        stack.append((neighbor, False))
# commit is likely to mark only this line as modified, but it's because I messed up a bit with branches. the run() method is fixed and should now work as expected. full fix can be reviewed at pull request num 44, commit num fb53f2866ce8a921bffe827af4d8bca7b72ae6ab                   


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

    plot_graph(G)


