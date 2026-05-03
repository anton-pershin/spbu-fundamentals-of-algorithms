
# Реализовать алгоритм Дейкстры.
#
# Алгоритм Дейкстры решает задачу поиска 
#  кратчайших путей на взвешенном графе.
#
# При работе алгоритма поддерживаются структуры данных:
#  - Словарь кратчайших путей `dist`
#  - Очередь с приоритетом для кратчайших путей `pq`.
#
# На очередной итерации алгоритма из очереди 
#  извлекается вершина с наименьшим кратчайшим путем.
#
# После этого в рамках той же итерации обновляются
#  кратчайшие расстояния до всех соседей извлеченной
#  вершины, обновленные вершины кладутся в `pq`.


from pathlib import Path
from typing import Any
# from abc import ABC, abstractmethod

# import numpy as np
import networkx as nx

from practicum_4.dfs import GraphTraversal 
from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class DijkstraAlgorithm(GraphTraversal):
    def __init__(self, G: AnyNxGraph) -> None:
        self.shortest_paths: dict[Any, list[Any]] = {}
        super().__init__(G)

    def previsit(self, node: Any, **params) -> None:
        """List of params:
        * path: list[Any] (path from the initial node to the given node)
        """
        self.shortest_paths[node] = params["path"]

    def postvisit(self, node: Any, **params) -> None:
        pass


    #*##########################

    def run(self, node: Any) -> None:

        import heapq

        # Лучшие найденные расстояния от
        #  `node` до каждой вершины
        dist = {node: 0}

        # (dist, node, path)
        pq: list[tuple[float, Any, list[Any]]] = [(0, node, [node])]

        while pq:

            # Вернуть кортеж с наименьшим `dist`.
            #  Для одинаковых `dist` вернуть "меньшую" вершину.
            this_dist, this_node, path = heapq.heappop(pq)

            if this_node in self.visited:
                continue

            self.visited.add(this_node)

            # `path` -> `self.shortest_paths[this_node]`.
            self.previsit(this_node, path=path)

            for neighbor in self.G.neighbors(this_node):

                # Приведение к float на случай строки.
                #  1 – для невзвешенного графа.
                weight = float(self.G[this_node][neighbor].get('weight', 1))
                new_dist = this_dist + weight

                if neighbor not in dist or new_dist < dist[neighbor]:
                    dist[neighbor] = new_dist
                    heapq.heappush(pq, (new_dist, neighbor, path + [neighbor]))

    #*##########################


if __name__ == "__main__":
    
    dir_path = Path("practicum_4/homework/plot/dijkstra/")

    G = nx.read_edgelist(
        Path("practicum_4") / "simple_weighted_graph_9_nodes.edgelist",
        create_using=nx.Graph
    )

    plot_graph(G, img_path = dir_path / "graph.png")

    sp = DijkstraAlgorithm(G)
    sp.run("0")

    for test_node in sp.shortest_paths:
        shortest_path_edges = [
            (
                sp.shortest_paths[test_node][i],
                sp.shortest_paths[test_node][i + 1]
            )
            for i in range(len(sp.shortest_paths[test_node]) - 1)
        ]

        plot_graph(
            G,
            img_path = dir_path / f"path_to_{test_node}.png",
            highlighted_edges = shortest_path_edges
        )
