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
        self.previsit(node)
        self.visited.add(node)

        for n_neigh in self.G.neighbors(node):
            if n_neigh not in self.visited:
                self.run(n_neigh)

        self.postvisit(node)


class DfsViaLifoQueue(GraphTraversal):
    def run(self, node: Any) -> None:
        stack = [node]
        while len(stack) > 0:
            node = stack.pop()
            if node not in self.visited:
                self.previsit(node)
                self.visited.add(node)
                for n_neigh in self.G.neighbors(node):
                    if n_neigh not in self.visited:
                        stack.append(n_neigh)


class DfsViaRecursionWithPrinting(DfsViaRecursion):
    def previsit(self, node: Any, **params) -> None:
        print(f"Previsit node {node}")

    def postvisit(self, node: Any, **params) -> None:
        print(f"Postvisit node {node}")

class DfsViaLifoQueueWithPrinting(DfsViaLifoQueue):
    def previsit(self, node: Any, **params) -> None:
        print(f"Previsit node {node}")

    def postvisit(self, node: Any, **params) -> None:
        print(f"Postvisit node {node}")


class TopologicalSorting(DfsViaLifoQueue):
    def __init__(self, G: AnyNxGraph) -> None:
        self.sorted.nodes: deque = deque()
        super().__init__(G)
    def reset(self) -> None:
        super().reset()
        self.sorted_nodes.clear()
    def sort(self, node: Any) -> list[Any]:
        self.run()
        sorted_nodes = list(self.sorted_nodes)
        self.reset()

        return sorted_nodes

if __name__ == "__main__":
    # Load and plot the graph
    G = nx.read_edgelist(
        Path("practicum_4") / "simple_graph_10_nodes.edgelist",
        create_using=nx.Graph
    )
    # plot_graph(G)

    # 1. Recursive DFS. Trivial to implement, but it does not scale on large graphs
    print("Recursive DFS")
    print("-" * 32)
    dfs = DfsViaRecursionWithPrinting(G)
    dfs.run(node="0")
    print()

    # 2. Iterative DFS. Makes use of LIFO/stack data structure, does scale on large graphs
    print("Iterative DFS")
    print("-" * 32)
    dfs = DfsViaLifoQueueWithPrinting(G)
    dfs.run(node="0")
    print()

    plot_graph(G)

    # 3. Postorder recursive DFS for topological sort
    # If a directed graph represent tasks to be done, the topological sort tells
    # us what the task order should be, i.e. scheduling
    G = nx.read_edgelist(Path("practicum_4") / "simple_graph_10_nodes.edgelist", create_using=nx.DiGraph)
    print("Topological sorting")
    print("-" * 32)
    ts = TopologicalSorting(G)
    sorted_nodes = ts.sort(node="0")
    print(sorted_nodes)
    plot_graph(G)

