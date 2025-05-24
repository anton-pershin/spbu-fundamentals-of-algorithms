from pathlib import Path
from collections import deque
from typing import Any
from abc import ABC, abstractmethod

import networkx as nx

from practicum_4.dfs import GraphTraversal
from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class DfsViaLifoQueueWithPostvisit(GraphTraversal):
    def __init__(self, G: GraphTraversal):
        self.G: GraphTraversal = G
        
    def run(self, node: Any) -> None:
        # Инициализация стека с начальным узлом
        stack = deque([node])
        # Множество для отслеживания посещенных узлов
        visited = set()

        while stack:
            # Извлечь узел из стека
            current_node = stack.pop()
            if current_node not in visited:
                # Отметить узел как посещённый
                visited.add(current_node)
                # Вызвать previsit перед обработкой
                self.previsit(current_node)

                # Добавить непосещённых соседей в стек
                for neighbor in self.graph.neighbors(current_node):
                    if neighbor not in visited:
                        stack.append(neighbor)
                
                # После обхода соседей вызвать postvisit
                self.postvisit(current_node)


class DfsViaLifoQueueWithPrinting(DfsViaLifoQueueWithPostvisit):
    def previsit(self, node: Any, **params) -> None:
        print(f"Previsit node {node}")

    def postvisit(self, node: Any, **params) -> None:
        print(f"Postvisit node {node}")


if __name__ == "__main__":
    # Load and plot the graph
    G = nx.read_edgelist(
        Path("practicum_4") / "simple_graph_10_nodes.edgelist",
        create_using=nx.Graph
    )
    # plot_graph(G)

    dfs = DfsViaLifoQueueWithPrinting(G)
    dfs.run(node="0")

