from pathlib import Path
from collections import deque
from typing import Any
from abc import ABC, abstractmethod

import networkx as nx

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph

class DisjointSets:
    def __init__(self) -> None:
        self.parent: dict[Any, Any] = {}
        self.rank: dict[Any, int] = {}

    def make_set(self, v: Any) -> None:
        """
        Creates a set of a single element
        """
        self.parent[v] = v
        self.rank[v] = 0

    def find(self, v: Any) -> Any:
        """
        Finds the set containing v without using recursion
        """
        if v not in self.parent:
            raise ValueError(f"Element {v} is not in any set")

        while self.parent[v] != v:
            v = self.parent[v]
        return v

    def union(self, u: Any, v: Any) -> None:
        """
        Unites the sets containing u and v using union by rank,
        i.e. we hang the smaller tree under the larger one
        """
        root_u = self.find(u)
        root_v = self.find(v)

        if root_u != root_v:
            if self.rank[root_u] > self.rank[root_v]:
                self.parent[root_v] = root_u
            elif self.rank[root_u] < self.rank[root_v]:
                self.parent[root_u] = root_v
            else:
                self.parent[root_v] = root_u
                self.rank[root_u] += 1
        else:
            raise ValueError(f"Elements {u} and {v} are already in the same set")
        
        

class KruskalAlgorithm:
    def __init__(self, G: AnyNxGraph) -> None:
        self.G: AnyNxGraph = G
        self.disjointsets = DisjointSets()
        self.edges = sorted(G.edges(data=True), key=lambda x: x[2]["weight"])
        self.mst_edges = set()


    def run(self) -> None:

        for node in self.G :
            self.disjointsets.make_set(node)

        for edge in self.edges:
            u,v,_ = edge
            if self.disjointsets.find(u) != self.disjointsets.find(v):
                self.disjointsets.union(u, v)
                self.mst_edges.add((u,v))
        


        
        


if __name__ == "__main__":
    G = nx.read_edgelist(
        Path("practicum_4") / "simple_weighted_graph_9_nodes.edgelist",
        create_using=nx.Graph
    )
    plot_graph(G)

    kruskal = KruskalAlgorithm(G)
    kruskal.run()

    plot_graph(G, highlighted_edges=list(kruskal.mst_edges))

