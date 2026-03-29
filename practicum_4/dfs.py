from pathlib import Path
from collections import deque
from typing import Any
from abc import ABC, abstractmethod

import networkx as nx

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class GraphTraversal(ABC):
    def __init__(self, G: AnyNxGraph) -> None:
        self.G: nx.Graph = G
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
        if node not in self.visited:
            self.previsit(node)
            self.visited.add(node)

            neighbors = self.G.neighbors(node)
            for neighbor in neighbors:
                if neighbor not in self.visited:
                    self.run(neighbor)
        self.postvisit(node)

class DfsViaLifoQueue(GraphTraversal):
    def run(self, node: Any) -> None:
        self.previsit(node)
        stack = deque([node])
        self.visited.add(node)

        while stack:
            neighbor = stack[-1]
            flag = 1
            for i in self.G.neighbors(neighbor):
                if i not in self.visited:
                    self.visited.add(i)
                    stack.append(i)
                    self.previsit(i)
                    flag = 0
                    break
            if flag:
                self.postvisit(stack.pop())


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


class TopologicalSorting(DfsViaRecursion):
    ##########################
    ### PUT YOUR CODE HERE ###
    #########################

    pass


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

