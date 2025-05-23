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
        stack = deque()
        stack.append((node, False))  # Очередь для "рассмотра" соседей. В начале состоит из одного узла.

        while len(stack) > 0:  # Пока очередь не пуста
            node, postvisit_flag = stack.pop()  # Возьмем узел из стака

            if postvisit_flag:  # Если узел уже был посещён до этого
                self.postvisit(node)  # Повторно обработаем узел уже после посещения
                continue

            if node not in self.visited:  # Если узел не был посещён
                self.previsit(node)  # Обработаем узел до его посещения, "посетим узел"

                self.visited.add(node)  # Добавим в посещённые
                stack.append((node, True))  # Вернём в стак, чтобы после повторно обработать

                for neighbor in self.G.neighbors(node):  # Рассмотрим соседей
                    if neighbor not in self.visited:
                        stack.append((neighbor, False))


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

