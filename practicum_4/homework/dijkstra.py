from pathlib import Path
from typing import Any
from abc import ABC, abstractmethod

import heapq
import numpy as np
import networkx as nx
import sys
sys.path.append(r"/Users/alexanderkuka/documents/python/pershin/spbu-fundamentals-of-algorithms")

from practicum_4.dfs import GraphTraversal 
from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class DijkstraAlgorithm(GraphTraversal):
    def __init__(self, G: AnyNxGraph) -> None:
        self.shortest_paths: dict[Any, list[Any]] = {}
        super().__init__(G)

    def previsit(self, node: Any, **params) -> None:
        self.shortest_paths[node] = params["path"]

    def postvisit(self, node: Any, **params) -> None:
        pass

    def run(self, start_node: Any) -> None:
        distances = {node: float('inf') for node in self.G.nodes()}
        distances[start_node] = 0
        self.shortest_paths = {start_node: [start_node]}
        
        heap = []
        heapq.heappush(heap, (0, start_node, [start_node]))

        while heap:
            current_dist, current_node, current_path = heapq.heappop(heap)
            
            if current_dist > distances[current_node]:
                continue

            self.previsit(current_node, path = current_path)
            self.visited.add(current_node)
            # print("visited:  ", self.visited)

            for neighbor in self.G.neighbors(current_node):
                if neighbor in self.visited:
                    continue
                    
                edge_weight = self.G[current_node][neighbor].get('weight')
                new_dist = current_dist + edge_weight
                
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist 
                    new_path = current_path + [neighbor]
                    heapq.heappush(heap, (new_dist, neighbor, new_path))
                    print((new_dist, neighbor, new_path))
            # print(distances)
            # print(" ")

        pass

if __name__ == "__main__":
    G = nx.read_edgelist(r"pershin/spbu-fundamentals-of-algorithms/practicum_4/simple_weighted_graph_9_nodes.edgelist")
    # plot_graph(G)

    sp = DijkstraAlgorithm(G)
    sp.run("0")

    test_node = "5"
    shortest_path_edges = [
        (sp.shortest_paths[test_node][i], sp.shortest_paths[test_node][i + 1])
        for i in range(len(sp.shortest_paths[test_node]) - 1)
    ]
    plot_graph(G, highlighted_edges=shortest_path_edges)

