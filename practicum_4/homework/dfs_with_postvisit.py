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
        #стек хранит пары(вершина,сост-ие)
        # 0-зашли в вер, 1 - выходим
        stack = [(node, 0)]

        while stack:
            curr, state = stack.pop()

            if state == 0:
                if curr in self.visited:
                    continue
                self.visited.add(curr)
                self.previsit(curr)

                #дальше вызовем postvisit
                stack.append((curr, 1))

                #доб соседей в обр.порядке
                for n in reversed(list(self.G.neighbors(curr))):
                    if n not in self.visited:
                        stack.append((n, 0))

            else:  #state == 1
                self.postvisit(curr)


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
