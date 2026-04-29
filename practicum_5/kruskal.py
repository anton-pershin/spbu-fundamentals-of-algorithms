from pathlib import Path
from collections import deque
from typing import Any
from abc import ABC, abstractmethod

import networkx as nx

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph

class DisjointSets:
    def __init__(self) -> None:

        ##########################
        ### PUT YOUR CODE HERE ###
        ##########################

        pass

    def make_set(self, v: Any) -> None:
        """
        Creates a set of a single element
        """

        ##########################
        ### PUT YOUR CODE HERE ###
        ##########################

        pass

    def find(self, v: Any) -> set[Any]:
        """
        Finds the set containing v without using recursion
        """

        ##########################
        ### PUT YOUR CODE HERE ###
        ##########################

        pass

    def union(self, u: Any, v: Any) -> None:
        """
        Unites the sets containing u and v using union by rank,
        i.e. we hang the smaller tree under the larger one
        """

        ##########################
        ### PUT YOUR CODE HERE ###
        ##########################

        pass
        

class KruskalAlgorithm:
    def __init__(self, G: AnyNxGraph) -> None:

        ##########################
        ### PUT YOUR CODE HERE ###
        ##########################

        pass

    def run(self) -> set[tuple[Any, Any]]:

        ##########################
        ### PUT YOUR CODE HERE ###
        ##########################

        pass


if __name__ == "__main__":
    G = nx.read_edgelist(
        Path("practicum_4") / "simple_weighted_graph_9_nodes.edgelist",
        create_using=nx.Graph
    )
    plot_graph(G)

    kruskal = KruskalAlgorithm(G)
    kruskal.run()

    plot_graph(G, highlighted_edges=list(kruskal.mst_edges))

