from pathlib import Path
from typing import Any
from abc import ABC, abstractmethod

import numpy as np
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

    def run(self, node: Any) -> None:
        # Инициализация расстояний и предшественников
        distances = {node: float('inf') for node in self.G.nodes()}
        distances[start_node] = 0
        predecessors = {start_node: None}
        # Множество непросмотренных узлов
        unvisited = set(self.G.nodes()) 

        while unvisited:
            # Выбор ближайшего незакрытого узла
            current_node = min(unvisited, key=lambda x: distances[x])
            
            # Убрать узел из множества неоптимальных
            unvisited.remove(current_node)
            
            # Пройти по соседям текущего узла
            for neighbor in self.G.neighbors(current_node):
                if neighbor not in unvisited:
                    continue
                
                # Рассчитать потенциальное улучшение пути
                edge_weight = self.G[current_node][neighbor].get('weight', 1)
                alternative_distance = distances[current_node] + edge_weight
                
                # Если найден лучший путь, обновить дистанцию и предшественника
                if alternative_distance < distances[neighbor]:
                    distances[neighbor] = alternative_distance
                    predecessors[neighbor] = current_node
        
        # Собрать кратчайшие пути
        for node in self.G.nodes():
            path = []
            current = node
            while current is not None:
                path.insert(0, current)
                current = predecessors.get(current)
            self.previsit(node, path=path)

if __name__ == "__main__":
    G = nx.read_edgelist(
        Path("practicum_4") / "simple_weighted_graph_9_nodes.edgelist",
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

