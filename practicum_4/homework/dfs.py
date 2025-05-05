from pathlib import Path
from collections import deque
from typing import Any
from abc import ABC, abstractmethod

import sys
sys.path.append(r"/home/viktoria/algoritms/spbu-fundamentals-of-algorithms")

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


from typing import Any

class DfsViaRecursion(GraphTraversal):
    def run(self, node: Any) -> None:
        self.visited.add(node)
        self.previsit(node)
        for neighbor_node in self.G.neighbors(node):
            if not neighbor_node in self.visited:
                self.run(neighbor_node)
        self.postvisit(node)

class DfsViaLifoQueue(GraphTraversal):
    def run(self, node: Any) -> None:
        the_stack = [node]
        while len(the_stack) > 0:
            current = the_stack[-1]
            if current not in self.visited:
                self.visited.add(current)
                self.previsit(current)
                neighbors_list = []
                for n in self.G.neighbors(current):
                    if not n in self.visited:
                        neighbors_list.append(n)
                if neighbors_list:
                    the_stack.extend(neighbors_list)
                else:
                    self.postvisit(current)
                    the_stack.pop()
            else:
                the_stack.pop()

class DfsViaRecursionWithPrinting(DfsViaRecursion):
    def previsit(self, node: Any, **params) -> None:
        print("Pre:", node)

    def postvisit(self, node: Any, **params) -> None:
        print("Post:", node)

class DfsViaLifoQueueWithPrinting(DfsViaLifoQueue):
    def previsit(self, node: Any, **params) -> None:
        print("Pre:", node)

    def postvisit(self, node: Any, **params) -> None:
        print("Post:", node)

class TopologicalSorting(DfsViaLifoQueue):
    def __init__(self, G: AnyNxGraph) -> None:
        super().__init__(G)
        self.sorted_order = []

    def postvisit(self, node: Any, **params) -> None:
        self.sorted_order.append(node)

    def sort(self, start_node: Any) -> list[Any]:
        self.reset()
        self.sorted_order = []
        super().run(start_node)
        return self.sorted_order[::-1]
    
    def previsit(self, node: Any, **params) -> None:
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

