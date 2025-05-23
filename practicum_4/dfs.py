from pathlib import Path
from collections import deque
from typing import Any
from abc import ABC, abstractmethod

import networkx as nx

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class GraphTraversal(ABC):
    def __init__(self, G: AnyNxGraph) -> None:
        self.G: AnyNxGraph = G
        self.visited: set[Any] = set()
        self.reset()
        
    def reset(self):
        self.visited.clear()

    @abstractmethod
    def previsit(self, node: Any, **params) -> None:
        pass

    @abstractmethod
    def postvisit(self, node: Any, **params) -> None:
        pass

    @abstractmethod
    def run(self, node: Any) -> None:
        pass


class DfsViaRecursion(GraphTraversal):
    def run(self, node: Any) -> None:
        self.visited.add(node)
        self.previsit(node)
        for adj_node in self.G.neighbors(node):
            if adj_node not in self.visited:
                self.run(adj_node)
        self.postvisit(node)


class DfsViaLifoQueue(GraphTraversal):
    def run(self, node: Any) -> None:
        stack = [node]
        while stack:
            top = stack[-1]
            if top not in self.visited:
                self.visited.add(top)
                self.previsit(top)
                to_visit = [neighbor for neighbor in self.G.neighbors(top) if neighbor not in self.visited]
                if to_visit:
                    stack.extend(to_visit)
                else:
                    self.postvisit(top)
                    stack.pop()
            else:
                stack.pop()


class DfsViaRecursionWithPrinting(DfsViaRecursion):
    def previsit(self, node: Any, **params) -> None:
        print(f"Previsit: {node}")

    def postvisit(self, node: Any, **params) -> None:
        print(f"Postvisit: {node}")


class DfsViaLifoQueueWithPrinting(DfsViaLifoQueue):
    def previsit(self, node: Any, **params) -> None:
        print(f"Previsit: {node}")

    def postvisit(self, node: Any, **params) -> None:
        print(f"Postvisit: {node}")


class TopologicalSorting(DfsViaLifoQueue):
    def __init__(self, G: AnyNxGraph) -> None:
        super().__init__(G)
        self.order: list[Any] = []

    def previsit(self, node: Any, **params) -> None:
        pass

    def postvisit(self, node: Any, **params) -> None:
        self.order.append(node)

    def sort(self, node: Any) -> list[Any]:
        self.reset()
        self.order = []
        super().run(node)
        return self.order[::-1]


if __name__ == "__main__":
    G = nx.read_edgelist(
        Path("practicum_4") / "simple_graph_10_nodes.edgelist",
        create_using=nx.Graph
    )

    print("Recursive DFS")
    print("-" * 32)
    dfs = DfsViaRecursionWithPrinting(G)
    dfs.run(node="0")
    print()

    print("Iterative DFS")
    print("-" * 32)
    dfs = DfsViaLifoQueueWithPrinting(G)
    dfs.run(node="0")
    print()

    plot_graph(G)

    G = nx.read_edgelist(Path("practicum_4") / "simple_graph_10_nodes.edgelist", create_using=nx.DiGraph)
    print("Topological sorting")
    print("-" * 32)
    ts = TopologicalSorting(G)
    sorted_nodes = ts.sort(node="0")
    print(sorted_nodes)
    plot_graph(G)