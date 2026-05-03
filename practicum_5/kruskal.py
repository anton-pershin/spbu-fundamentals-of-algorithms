from pathlib import Path
from collections import deque
from typing import Any
from abc import ABC, abstractmethod

import networkx as nx

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph

class DisjointSets:
    def __init__(self) -> None:
        self.parent: dict[Any, Any] = dict()
        self.rank: dict[Any, int] = dict()

    def make_set(self, v: Any) -> None:
        self.parent[v] = v
        self.rank[v] = 0

    def find(self, v: Any) -> set[Any]:
        current_node = v
        while self.parent[current_node] != current_node:
            current_node = self.parent[current_node]
        return set(current_node)

    def union(self, u: Any, v: Any) -> None:
        root_u = list(self.find(u))[0]
        root_v = list(self.find(v))[0]

        if root_u == root_v:
            return
        else:
            if self.rank[root_u] > self.rank[root_v]:
                self.parent[root_v] = root_u
            elif self.rank[root_u] < self.rank[root_v]:
                self.parent[root_u] = root_v
            else:
                self.parent[root_u] = root_v
                self.rank[root_v] += 1

        

class KruskalAlgorithm:
    def __init__(self, G: AnyNxGraph) -> None:
        self.G = G
        self.Djs = DisjointSets()
        self.edges = sorted(G.edges(data='weight', default=1), key=lambda x: x[2])
    def run(self) -> set[tuple[Any, Any]]:
        for node in self.G:
            self.Djs.make_set(node)
        
        result = set()
        for edge in self.edges:
            first, second, length = edge
            if self.Djs.find(first) != self.Djs.find(second):
                self.Djs.union(first, second)
                result.add(tuple(sorted((first, second))))
        self.mst_edges = result
        return result


if __name__ == "__main__":
    G = nx.read_edgelist(
        Path("practicum_4") / "simple_weighted_graph_9_nodes.edgelist",
        create_using=nx.Graph
    )
    plot_graph(G)

    kruskal = KruskalAlgorithm(G)
    kruskal.run()

    plot_graph(G, highlighted_edges=list(kruskal.mst_edges))

