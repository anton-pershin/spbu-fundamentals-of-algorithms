from pathlib import Path
from collections import deque
from typing import Any
from abc import ABC, abstractmethod

import networkx as nx

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph

class DisjointSets:
    def __init__(self) -> None:
        self.parents: dict[Any, Any] = {}
        self.ranks: dict[Any, Any] = {}

    def make_set(self, v: Any) -> None:
        self.parents[v] = v
        self.ranks[v] = 0

    def find(self, v: Any) -> Any:
        if v not in self.parents:
            raise ValueError("error")

        # path compression
        root = v
        while self.parents[root] != root:
            root = self.parents[root]
        
        while v != root:
            next_v = self.parents[v]
            self.parents[v] = root
            v = next_v
        
        return root

    def union(self, u: Any, v: Any) -> None:
        root_u = self.find(u)
        root_v = self.find(v)

        if root_v != root_u:
            if self.ranks[root_u] > self.ranks[root_v]:
                self.parents[root_v] = root_u
            elif self.ranks[root_u] < self.ranks[root_v]:
                self.parents[root_u] = root_v
            else:
                self.parents[root_u] = root_v
                self.ranks[root_v] += 1


class KruskalAlgorithm:
    def __init__(self, G: AnyNxGraph) -> None:
        self.G: AnyNxGraph = G
        self.disjoint_sets: DisjointSets = DisjointSets()
        self.edges = sorted(G.edges(data=True), key=lambda x: x[2]["weight"])
        self.mst_edges: set[tuple[Any, Any]] = set()

    def run(self) -> set[tuple[Any, Any]]:
        for v in self.G.nodes():
            self.disjoint_sets.make_set(v)

        for u, v, data in self.edges:
            if self.disjoint_sets.find(u) != self.disjoint_sets.find(v):
                self.disjoint_sets.union(u, v)
                self.mst_edges.add((u, v))
        
        return self.mst_edges


if __name__ == "__main__":
    G = nx.read_edgelist(
        Path("practicum_4") / "simple_weighted_graph_9_nodes.edgelist",
        create_using=nx.Graph
    )
    plot_graph(G)

    kruskal = KruskalAlgorithm(G)
    kruskal.run()

    plot_graph(G, highlighted_edges=list(kruskal.mst_edges))