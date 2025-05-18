from pathlib import Path
from collections import deque
from typing import Any
from abc import ABC, abstractmethod

import networkx as nx

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph

class DisjointSets:
    def __init__(self) -> None:
        # maps an element to its partent
        self.parents: dict[Any, Any] = {}

        #maps an eleent to its parent
        self.ranks: dict[Any, int] = {}

    def make_set(self, v: Any) -> None:
        self.parents[v] = v
        self.ranks[v] = 0
        
    def find(self, v: Any) -> Any:
        while v != self.parents[v]:
            v = self.parents[v]
        return v
    
    def union(self, u: Any, v: Any) -> None:
        u_root = self.find(u)
        v_root = self.find(v)
        if u_root != v_root:
            u_rank = self.ranks[u_root]
            v_rank = self.ranks[v_root]
            if u_rank > v_rank:
                self.parents[v_root] = u_root
            elif u_rank < v_rank:
                self.parents[u_root] = v_root
            else:
                self.parents[u_root] = v_root
                self.ranks[v_root] += 1

class KruskalAlgorithm:
    def __init__(self, G: AnyNxGraph) -> None:
        self.G: AnyNxGraph = G
        self.disjoint_sets: DisjointSets = DisjointSets()
        self.edges = sorted(G.edges(data=True), key=lambda x: x[2]["weight"])
        self.mst_edges: set[tuple[Any, Any]] = set()

    def run(self) -> set[tuple[Any, Any]]:
        for i in self.G.nodes:
            self.disjoint_sets.make_set(i)
        
        for i in self.G.edges:
            if self.disjoint_sets.find(i[0]) != self.disjoint_sets.find(i[1]):
                self.mst_edges.add(i)
                self.disjoint_sets.union(i[0], i[1])
                



if __name__ == "__main__":
    G = nx.read_edgelist(
        Path("practicum_4") / "simple_weighted_graph_9_nodes.edgelist",
        create_using=nx.Graph
    )
    plot_graph(G)

    kruskal = KruskalAlgorithm(G)
    kruskal.run()

    plot_graph(G, highlighted_edges=list(kruskal.mst_edges))
