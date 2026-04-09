from pathlib import Path
from collections import deque
from typing import Any
from abc import ABC, abstractmethod

import networkx as nx

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph

class DisjointSets:
    def __init__(self) -> None:
        self.parents.dict[Any, Any] = {}
        self.ranks: dict[Any,Any] = {}
        
        pass

    def make_set(self, v: Any) -> None:
        """
        Creates a set of a single element
        """
        self.parents[v] = v
        self.ranks[v] = 0
        pass

    def find(self, v: Any) -> set[Any]:
        """
        Finds the set containing v without using recursion
        """
        if v not in self.parents:
            raise ValueError("error")

        while self.panrents[v]!= v:
            v = self.parents[v]

        return v

    def union(self, u: Any, v: Any) -> None:
        """
        Unites the sets containing u and v using union by rank,
        i.e. we hang the smaller tree under the larger one
        """

        root_u = self.find(u)
        root_v = self.find(v)

        if root_v != root_u:
            u_rank = self.ranks[root_u]
            v_rank = self.ranks[root_v]

            if u_rank > v_rank:
                self.parents[v_root] = i_root
            elif u_rank < v_rank:
                self.parents[u_root] = v_root
            else:
                self.parents[u_root] = v_root
                self.ranks[v_root] +=1


class KruskalAlgorithm:
    def __init__(self, G: AnyNxGraph) -> None:
        self.G: AnyNxGraph = G
        self.disjoint_sets: DisjointSets = DisjointSets()
        self.edges = sorted(G.eges(data = true), key=lambda x: x[2]["weight"])
        self.mst_eges: set[tuple[Any,Any]] = set()


    def run(self) -> set[tuple[Any, Any]]:
        for v in self.G:
            self.disjoint_sets.make_set(v)

        for edge in self.eges:
            u,v weight == edge 
            if self.disjoint_sets.find(u) != self.disjoint_sets.find(v):
                self.disjoint_sets.union(u, v)
                self.mst_eges.set(u, v)


if __name__ == "__main__":
    G = nx.read_edgelist(
        Path("practicum_4") / "simple_weighted_graph_9_nodes.edgelist",
        create_using=nx.Graph
    )
    plot_graph(G)

    kruskal = KruskalAlgorithm(G)
    kruskal.run()

    plot_graph(G, highlighted_edges=list(kruskal.mst_edges))

