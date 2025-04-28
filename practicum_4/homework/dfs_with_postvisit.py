import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

from collections import deque
from typing import Any
from abc import ABC, abstractmethod

import networkx as nx

from practicum_4.dfs import GraphTraversal
from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class DfsViaLifoQueueWithPostvisit(GraphTraversal):
    def run(self, node: Any) -> None:
        # множество посещенных вершин
        visited: set[Any] = set()
        # вершина, итератор по соседям, путь до вершины
        stack: list[tuple[Any, Any, list[Any]]] = []

        visited.add(node)
        initial_path = [node]
        self.previsit(node, path=initial_path)

        stack.append((node, iter(self.G.neighbors(node)), initial_path))

        while stack:
            current, neighbors_iter, path_to_current = stack[-1]
            try:
                neighbor = next(neighbors_iter)
                # если не посетили - обрабатываем
                if neighbor not in visited:
                    visited.add(neighbor)
                    new_path = path_to_current + [neighbor]
                    self.previsit(neighbor, path=new_path)
                    stack.append((neighbor, iter(self.G.neighbors(neighbor)), new_path))
                # если посетили - пропускаем
            except StopIteration:
                # если все соседи рассмотрены
                self.postvisit(current, path=path_to_current)
                stack.pop()



class DfsViaLifoQueueWithPrinting(DfsViaLifoQueueWithPostvisit):
    def previsit(self, node: Any, **params) -> None:
        print(f"Previsit node {node}")

    def postvisit(self, node: Any, **params) -> None:
        print(f"Postvisit node {node}")


if __name__ == "__main__":
    # Load and plot the graph
    G = nx.read_edgelist(
        project_root / "practicum_4" / "simple_graph_10_nodes.edgelist",
        create_using=nx.Graph
    )
    # plot_graph(G)

    dfs = DfsViaLifoQueueWithPrinting(G)
    dfs.run(node="0")

