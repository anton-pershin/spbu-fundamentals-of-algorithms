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
        self.ranks: dict[Any, int] = {}

    def make_set(self, v: Any) -> None:
        """
        Creates a set of a single element
        """
        self.parents[v] = v
        self.ranks[v] = 0

    def find(self, v: Any) -> Any:
        """
        Finds the set containing v without using recursion
        """
        if v not in self.parents:
            raise ValueError(f"Node {v} is not in the graph")
        while self.parents[v] != v:
            v = self.parents[v]
        return v
        

    def union(self, u: Any, v: Any) -> None:
        """
        Unites the sets containing u and v using union by rank,
        i.e. we hang the smaller tree under the larger one
        """

        par_u, par_v = self.find(u), self.find(v)
        if par_u != par_v:
            u_rank = self.ranks[par_u]
            v_rank = self.ranks[par_v]

            if u_rank > v_rank:
                self.parents[par_v] = par_u
            elif v_rank > u_rank:
                self.parents[par_u] = par_v
            else:
                self.parents[par_u] = par_v
                self.ranks[par_v] += 1
        

class KruskalAlgorithm:
    def __init__(self, G: AnyNxGraph) -> None:
        self.G: AnyNxGraph = G
        self.disjoint_sets: DisjointSets = DisjointSets()
        self.edges = sorted(G.edges(data=True), key=lambda x: x[2]["weight"])
        self.mst_edges = set()

    def run(self) -> set[tuple[Any, Any]]:    
        for v in self.G:
            self.disjoint_sets.make_set(v)
        for edge in self.edges:
            u, v, _ = edge
            if self.disjoint_sets.find(u) != self.disjoint_sets(v):
                self.disjoint_sets.union(u, v)
                self.mst_edges.add(u, v)
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

