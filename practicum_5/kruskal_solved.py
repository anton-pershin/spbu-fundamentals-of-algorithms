from pathlib import Path
from collections import deque
from typing import Any

import networkx as nx

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph

class DisjointSets:
    def __init__(self) -> None:
        # DisjointSets.parents maps an element to its parent
        # If an element points to itself, this element is a root of
        # the oriented tree
        # The whole orinted tree is a single set in DisjointSets
        # and the aforementioned element is thus associated with this set
        # => when we are asked to return a set, we actually return 
        # its root element
        self.parents: dict[Any, Any] = {} # maps node to its parent 
        # DisjointSets.ranks maps an element to its rank
        # The rank of a tree is the number of edges in the longest
        # path from the root to a leaf
        self.ranks: dict[Any, int] = {}

    def make_set(self, v: Any) -> None:
        """
        Creates a set of a single element
        """
        self.parents[v] = v
        self.ranks[v] = 0

    def find(self, v: Any) -> set[Any]:
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
        u_root = self.find(u)
        v_root = self.find(v)
        if u_root != v_root:  # u and v are in different sets
            # Use ranks to determine the root of the tree
            # with the largest rank
            # Note that the rank only needs to be incremented
            # if two roots have the same rank
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
        self.mst_edges = set()

    def run(self) -> set[tuple[Any, Any]]:
        for v in self.G:
            self.disjoint_sets.make_set(v)

        for edge in self.edges:  # note that they are sorted 
            u, v, weight = edge
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

