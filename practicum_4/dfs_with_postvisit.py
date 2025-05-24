from typing import Any
from abc import ABC, abstractmethod

import networkx as nx

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph

class GraphTraversal(ABC):
    def __init__(self, G: AnyNxGraph) -> None:
        self.G: AnyNxGraph = G
        self.visited: set[Any] = set()
        self.visited_previsit: set[Any] = set()
        self.visited_postvisit: set[Any] = set()
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

class DfsViaLifoQueueWithPostvisit(GraphTraversal):
    def previsit(self, node: Any, **params) -> None:
        print(f"Previsit {node}")
    def postvisit(self, node: Any, **params) -> None:
        print(f"Postvisit {node}")
    def run(self, G, node: Any) -> None:
        stack = [node]
        visited_postvisit = set()

        while len(stack) > 0:
            node = stack[-1]

            if node not in self.visited:
                self.previsit(node)
                self.visited.add(node)

                for n_neigh in G.neighbors(node):
                    if n_neigh not in self.visited:
                        stack.append(n_neigh)
            else:
                if node not in visited_postvisit:
                    self.postvisit(node)
                    visited_postvisit.add(node)
                stack.pop()



if __name__ == "__main__":
    # Load and plot the graph
    G = nx.read_edgelist(
        "simple_graph_10_nodes.edgelist",
        create_using=nx.Graph
    )
    # plot_graph(G)

    print("Iterative DFS")
    print("-" * 32)
    dfs = DfsViaLifoQueueWithPostvisit(G)
    dfs.run(node="0")
    print()

    plot_graph(G)

