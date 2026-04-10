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
        self.ranks: dict[Any, int] = {}

    def make_set(self, v: Any) -> None:
        """
        Creates a set of a single element
        """
        self.parent[v] = v
        self.ranks[v] = 0

    def find(self, v: Any) -> set[Any]:
        """
        Finds the set containing v without using recursion
        """
        if v not in self.parent:
            raise ValueError("not in set")
        while self.parent[v] != v:
            v = self.parent[v]

        return v


    def union(self, u: Any, v: Any) -> None:
        """
        Unites the sets containing u and v using union by rank,
        i.e. we hang the smaller tree under the larger one
        """
        u_root = self.find(u)
        v_root = self.find(v)

        if(u_root != v_root):
            if self.ranks[u_root] > self.ranks[v_root]:
                self.parent[v_root] = u_root
            elif self.ranks[u_root] < self.ranks[v_root]:
                self.parent[u_root] = v_root

            else:
                self.ranks[u_root] += 1
                self.parent[v_root] = u_root
        

class KruskalAlgorithm:
    def __init__(self, G: AnyNxGraph) -> None:
        self.G: AnyNxGraph = G
        self.disjoint_sets: DisjointSets = DisjointSets()
        self.edges = sorted(G.edges(data=True), key=lambda x: x[2]["weight"])
        self.mst_edges: set[tuple[Any, Any]] = set()

    def run(self) -> None:
        for u in self.G:
            self.disjoint_sets.make_set(u)

        for e in self.edges:
            u, v, weight = e
            if self.disjoint_sets.find(u) != self.disjoint_sets.find(v):
                self.disjoint_sets.union(u, v)
                self.mst_edges.add((u, v))



if __name__ == "__main__":
    G = nx.read_edgelist(
        Path("practicum_4") / "simple_weighted_graph_9_nodes.edgelist",
        create_using=nx.Graph
    )
    plot_graph(G)

    kruskal = KruskalAlgorithm(G)
    kruskal.run()

    plot_graph(G, highlighted_edges=list(kruskal.mst_edges))

