from pathlib import Path
from typing import Any
from abc import ABC, abstractmethod

import numpy as np
import networkx as nx

from practicum_4.dfs import GraphTraversal 
from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph

# There was no suitable enough lib for my aims
# So I made it myself
# It may be a little clumsy, yet it works
class PriorityQueue():
    def __init__(self) -> None:
        self.data: list(tuple()) = list()

    def __repr__(self) -> str():
        return f"{self.data}"

    def __contains__(self, key) -> bool():
        for item in self.data:
            if item[0] == key:
                return True
        return False

    def notempty(self) -> bool:
        return len(self.data) != 0

    def add(self, item) -> None:
        self.data.append(item)
        self.data = sorted(self.data, key = lambda item: item[1])
    
    def get(self, key) -> tuple():
        for item in self.data:
            if item[0] == key:
                return item

    def pop(self) -> tuple():
        item = self.data.pop(0)
        return item
    
    def change(self, key, value) -> tuple():
        for i in range(len(self.data)):
            itemKey = self.data[i][0]
            if itemKey == key:
                self.data[i] = (itemKey, value)
                return True
        return False



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
        pq = PriorityQueue()
        paths: dict[Any, list[Any]] = {}
        
        pq.add((node, 0))
        paths[node] = [node]
        
        while pq.notempty() == True:
            cur, curDist = pq.pop()
            self.visited.add(cur)
            self.previsit(cur, path = paths[cur])
            
            for neighbor in G.neighbors(cur):
                # Calculate overall distance from beginning to this exact neighbor
                neighborDist = curDist + G.edges[cur, neighbor]["weight"] 
                if neighbor in pq:
                    if neighborDist < pq.get(neighbor)[1]:

                        pq.change(neighbor, neighborDist)
                        paths[neighbor] = paths[cur] + [neighbor]

                elif neighbor not in self.visited:
                    pq.add((neighbor, neighborDist))
                    paths[neighbor] = paths[cur] + [neighbor]


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

