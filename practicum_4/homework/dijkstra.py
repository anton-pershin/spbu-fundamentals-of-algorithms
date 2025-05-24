import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

from typing import Any
from abc import ABC, abstractmethod

import numpy as np
import networkx as nx
import heapq

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

    def run(self, node: Any) -> None:
        distances: dict[Any, float] = {}
        # расстояние, вершина, путь от старта
        priority_queue: list[tuple[float, Any, list[Any]]] = []

        distances[node] = 0.0
        initial_path = [node]
        # сохраняем стартовый путь
        self.previsit(node, path=initial_path)
        heapq.heappush(priority_queue, (0.0, node, initial_path))

        while priority_queue:
            current_dist, current_node, path_to_node = heapq.heappop(priority_queue)

            # если нашли лучший путь - пропускаем
            if current_dist > distances.get(current_node, float('inf')):
                continue

            # Проход по соседям
            for neighbor in self.G.neighbors(current_node):
                # получаем вес ребра
                weight = self.G[current_node][neighbor].get("weight", 1.0)
                new_dist = current_dist + weight

                if new_dist < distances.get(neighbor, float('inf')):
                    distances[neighbor] = new_dist
                    new_path = path_to_node + [neighbor]
                    # сохраняем новый путь
                    self.previsit(neighbor, path=new_path)
                    # добавляем в очередь
                    heapq.heappush(priority_queue, (new_dist, neighbor, new_path))

if __name__ == "__main__":
    G = nx.read_edgelist(
        project_root / "practicum_4" / "simple_weighted_graph_9_nodes.edgelist",
        create_using=nx.Graph
    )
    plot_graph(G)

    sp = DijkstraAlgorithm(G)
    sp.run("0")

    test_node = "5"
    shortest_path_edges = [
        (sp.shortest_paths[test_node][i], sp.shortest_paths[test_node][i + 1])
        for i in range(len(sp.shortest_paths[test_node]) - 1)
    ]
    plot_graph(G, highlighted_edges=shortest_path_edges)

