from pathlib import Path
from collections import deque
from typing import Any
from abc import ABC, abstractmethod

import networkx as nx

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph

class DisjointSets:
    def __init__(self) -> None:
        self.parents = {}
        self.ranks = {}

    def make_set(self, v: Any) -> None:
        self.parents[v] = v
        self.ranks[v] = 0

    def find(self, v: Any) -> set[Any]:
        if v not in self.parents:
            raise ValueError()
        while self.parents[v] != v:
            v = self.parents[v]
        return v

    def union(self, u: Any, v: Any) -> None:
        root_u = self.find(u)
        root_v = self.find(v)

        if root_u != root_v:
            u_rank = self.ranks[root_u]
            v_rank = self.ranks[root_v]

            if u_rank > v_rank:
                self.parents[root_v] = root_u
            elif v_rank > u_rank:
                self.parents[root_u] = root_v
            else:
                self.parents[root_u] = root_v
                self.ranks[root_v] += 1


        

class KruskalAlgorithm:
    def __init__(self, G: AnyNxGraph) -> None:
        self.G = G
        self.disjoint_sets: DisjointSets = DisjointSets()
        self.edges = sorted(G.edges(data=True), key=lambda x: x[2]["weight"])
        self.mst_edges: set[tuple[Any, Any]] = set()

    def run(self) -> set[tuple[Any, Any]]:

        for i in self.G.nodes():
            self.disjoint_sets.make_set(i)
        for i, j, k in self.edges:
            if self.disjoint_sets.find(i) != self.disjoint_sets.find(j):
                self.mst_edges.add((i, j))
                self.disjoint_sets.union(i, j)





if __name__ == "__main__":
    G = nx.read_edgelist(
        Path("..") / "practicum_4" / "simple_weighted_graph_9_nodes.edgelist",
        create_using=nx.Graph
    )
    plot_graph(G)

    kruskal = KruskalAlgorithm(G)
    kruskal.run()

    plot_graph(G, highlighted_edges=list(kruskal.mst_edges))

