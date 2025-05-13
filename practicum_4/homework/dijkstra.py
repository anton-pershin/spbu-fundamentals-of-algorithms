from pathlib import Path
from typing import Any
from abc import ABC, abstractmethod
from collections import defaultdict
from heapq import heappop, heappush


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

    def run(self) -> None:
        def dijkstra_all_paths(graph, start):
            distances = {node: float('inf') for node in graph.nodes()}
            distances[start] = 0
            predecessors = defaultdict(list)
            heap = [(0, start)]
            # print("*"*20, '\n', graph.nodes())
            
            while heap:
                current_dist, u = heappop(heap)
                if current_dist > distances[u]:
                    continue
                for v in graph.neighbors(u):
                    weight = graph[u][v].get('weight', 1)
                    new_dist = current_dist + weight
                    if new_dist < distances[v]:
                        distances[v] = new_dist
                        predecessors[v] = [u]
                        heappush(heap, (new_dist, v))
                    elif new_dist == distances[v]:
                        predecessors[v].append(u)
            return distances, predecessors
    
        def get_all_paths(predecessors, start, end):
            paths = []
            def dfs(node, path):
                if node == start:
                    paths.append(list(reversed(path)))
                    return
                for pred in predecessors[node]:
                    dfs(pred, path + [pred])
            dfs(end, [end])
            return paths
        
        all_paths = dict()
        n = len(self.G)
        for start_node in range(n):
            start_node = str(start_node)
            distances, predcessors = dijkstra_all_paths(self.G, start_node)
            all_paths_from_node = [get_all_paths(predcessors, start_node, str(end_node)) for end_node in range(n)]
            all_paths[start_node] = all_paths_from_node
        
        self.shortest_paths = all_paths
        
        


if __name__ == "__main__":
    G = nx.read_edgelist(
        Path("practicum_4") / "simple_weighted_graph_9_nodes.edgelist",
        create_using=nx.Graph
    )
    plot_graph(G)

    sp = DijkstraAlgorithm(G)
    sp.run()

    start_node = '0'
    test_node = 5
    # print(sp.shortest_paths['0'][5][0])
    shortest_path_edges = [(sp.shortest_paths[start_node][test_node][0][i], sp.shortest_paths[start_node][test_node][0][i+1]) for i in range(len( sp.shortest_paths[start_node][test_node][0])-1)]
    # print(shortest_path_edges)
    plot_graph(G, highlighted_edges=shortest_path_edges) 

