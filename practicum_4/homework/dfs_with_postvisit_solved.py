
# Реализовать обход графа в глубину без использования 
#  рекурсии, с вызовами previsit и postvisit методов.

# def dfs(node):
#   visited.add(node)
#   previsit(node)
#   for neighbors:
#     if neighbor not in visited:
#       dfs(neighbor)
#   postvisit(node)


from pathlib     import Path
from collections import deque
from typing      import Any
# from abc import ABC, abstractmethod

import networkx as nx

from practicum_4.dfs     import GraphTraversal
from src.plotting.graphs import plot_graph
from src.common          import AnyNxGraph


class DfsViaLifoQueueWithPostvisit(GraphTraversal):

    def __init__(self, G: AnyNxGraph) -> None:
        self.dfs_paths: dict[Any, list[Any]] = {}
        super().__init__(G)

    def reset(self) -> None:
        super().reset()
        self.dfs_paths.clear()


    #*##########################

    def run(self, node: Any) -> None:

        # Инициализируем `stack` первой вершиной.
        #  Потом – только цикл.
        stack: deque[tuple[Any, bool, list[Any]]] = \
               deque([(node, False, [node])])
        
        # Пока в `stack` что-то есть ...
        while stack:

            # Взять последний добавленный кортеж (LIFO)
            this_node, is_processed, path = stack.pop()

            # Если вершина была обработана:
            #  возвражаемся после обработки соседей.
            #
            if is_processed:

                # Виртуальный метод из `Dfs...Printing`
                #  печатает "Postvisit node X".
                #
                self.postvisit(this_node, path=path)
                continue

            if this_node in self.visited:
                #
                #  Рассмотрим случай
                #   "!is_processed && visited"
                #  
                #  На прошлой итерации стека алгоритм положил
                #   рассматриваемую вершину наверх.
                #  
                #  Но эта вершина может уже лежать глубже в стеке. 
                #   При этом `stack` не обладает глобальной памятью.
                #    Чтобы избежать дубликатов – используем `set`.
                #
                continue

            self.visited.add(this_node)

            # Сохранить `path` в поле объекта, 
            #  чтобы вызывающий код мог прочитать 
            #   результат после `dfs.run()`.
            #
            self.dfs_paths[this_node] = path

            # Вызывается один раз, при первом рассмотрении.
            #  Зафиксировать путь для данной вершины и 
            #   сообщить об этом.
            #
            self.previsit(this_node, path=path)

            stack.append((this_node, True, path))

            # Отправить в `stack` соседей, которых
            #  которых еще не посетили.
            #
            for neighbor in self.G.neighbors(this_node):
                if neighbor not in self.visited:
                    stack.append((neighbor, False, path + [neighbor]))

    #*##########################


class DfsViaLifoQueueWithPrinting(DfsViaLifoQueueWithPostvisit):
    def previsit(self, node: Any, **params) -> None:
        print(f"Previsit node {node}")

    def postvisit(self, node: Any, **params) -> None:
        print(f"Postvisit node {node}")


if __name__ == "__main__":

    dir_path = Path("practicum_4/homework/plot/dfs/")

    G = nx.read_edgelist(
        Path("practicum_4") / "simple_graph_10_nodes.edgelist",
        create_using=nx.Graph
    )

    plot_graph(G, img_path=dir_path / "graph.png")

    dfs = DfsViaLifoQueueWithPrinting(G)
    dfs.run(node="0")

    # Ребра, по которым dfs открывал каждую вершину.
    #  Для каждой вершины такое ребро — последний
    #   шаг пути = (path[-2], path[-1]).
    #    Условие len() > 1 исключает стартовую вершину.
    #
    dfs_tree_edges = [
        (dfs.dfs_paths[node][-2], dfs.dfs_paths[node][-1])
        for node in dfs.dfs_paths
        if len(dfs.dfs_paths[node]) > 1
    ]

    plot_graph(
        G,
        img_path = dir_path / "dfs_tree.png",
        highlighted_edges = dfs_tree_edges
    )
