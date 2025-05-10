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
        new_G = nx.Graph()
        new_G.add_node(node)

        self.visited.add(node)
        paths = {v: 100 for v in G.nodes()}
        f_paths = {v: 100 for v in G.nodes()}
        i = 100
        for neighbor in self.G.neighbors(node):
            paths[neighbor] = G[node][neighbor]['weight']
            f_paths[neighbor] = G[node][neighbor]['weight']

        while len(self.visited) != len(G.nodes()):
            min_len = 100
            for neighbor, length in paths.items():
                if length < min_len:
                    min_len = length
                    next_v = neighbor
            if next_v in self.G.neighbors(node):
                new_G.add_edge(node, next_v, weight=G[node][next_v]['weight'])
            self.visited.add(next_v)
            #paths[next_v] = i
            for neighbor_of_n in self.G.neighbors(next_v):
                if neighbor_of_n not in self.visited:
                    if f_paths[next_v] + G[next_v][neighbor_of_n]['weight'] < f_paths[neighbor_of_n]:
                        f_paths[neighbor_of_n] = f_paths[next_v] + G[next_v][neighbor_of_n]['weight']
                        if new_G.has_node(neighbor_of_n):
                            new_G.remove_node(neighbor_of_n)
                        new_G.add_edge(next_v, neighbor_of_n, weight=G[next_v][neighbor_of_n]['weight'])

                    if G[next_v][neighbor_of_n]['weight'] < paths[neighbor_of_n]:
                        paths[neighbor_of_n] = G[next_v][neighbor_of_n]['weight']
                else:
                    paths[neighbor_of_n] = i
        plot_graph(new_G)
    # в f_paths хранятся минимальные расстояния от node до вершин графа
    # new_G - итоговый граф



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

