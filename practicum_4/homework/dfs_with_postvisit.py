import sys
from pathlib import Path

from networkx.classes import neighbors

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
        # вершина, состояние(enter, exit), путь до вершины
        stack: list[ tuple[ Any, str, list[Any] ] ] = [ ( node, 'enter', [node] ) ]

        while stack:
            current, state, path = stack.pop()

            if state == 'enter':
                if current in visited:
                    continue
                visited.add(current)
                self.previsit(current, path=path)
                stack.append( (current, 'exit', path) )
                neighbors = list(self.G.neighbors(current))
                for neighbor in reversed(neighbors): # фикс порядка обхода (reversed)
                    if neighbor not in visited:
                        new_path = path + [neighbor]
                        stack.append( (neighbor, 'enter', new_path) )

            else:
                self.postvisit(current, path=path)

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
    plot_graph(G)

    dfs = DfsViaLifoQueueWithPrinting(G)
    dfs.run(node="0")

