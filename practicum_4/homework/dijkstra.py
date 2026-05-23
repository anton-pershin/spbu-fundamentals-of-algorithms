from pathlib import Path
from typing import Any
from abc import ABC, abstractmethod
import heapq 

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
        self.shortest_paths[node] = params["path"]

    def postvisit(self, node: Any, **params) -> None:
        pass

    def run(self, node: Any) -> None:
        distances = {}
        for vertex in self.G.nodes():
            distances[vertex] = float('inf')
        distances[node] = 0  
        
        pq = [(0, node, [node])]
        
        processed = set()
        
        while pq:
            current_dist, current_node, current_path = heapq.heappop(pq)
            
            if current_node in processed:
                continue
            
            if current_dist > distances[current_node]:
                continue
            
            processed.add(current_node)
            self.previsit(current_node, path=current_path)
            
            for neighbor in self.G.neighbors(current_node):
                if neighbor in processed:
                    continue
                
                edge_data = self.G.get_edge_data(current_node, neighbor)
                weight = edge_data.get('weight', 1)
                
                new_dist = current_dist + weight
                
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    new_path = current_path + [neighbor]
                    heapq.heappush(pq, (new_dist, neighbor, new_path))
              

if __name__ == "__main__":
    G = nx.read_edgelist(
        Path("practicum_4") / "simple_weighted_graph_9_nodes.edgelist",
        create_using=nx.Graph
    )
    plot_graph(G)

    sp = DijkstraAlgorithm(G)
    sp.run("0")

    test_node = "5"
    if test_node in sp.shortest_paths:
        shortest_path_edges = [
            (sp.shortest_paths[test_node][i], sp.shortest_paths[test_node][i + 1])
            for i in range(len(sp.shortest_paths[test_node]) - 1)
        ]
        print(f"Кратчайший путь от 0 до {test_node}: {sp.shortest_paths[test_node]}")
        plot_graph(G, highlighted_edges=shortest_path_edges)
