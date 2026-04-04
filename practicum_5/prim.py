from pathlib import Path
import heapq
from typing import Any
from abc import ABC, abstractmethod

import networkx as nx
import numpy as np

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class PrimAlgorithm:
    def __init__(self, G: AnyNxGraph) -> None:

        ##########################
        ### PUT YOUR CODE HERE ###
        ##########################

        pass

    def run(self, node: Any) -> None:

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

    prim = PrimAlgorithm(G)
    mst_edges = prim.run(node="0")

    plot_graph(G, highlighted_edges=list(prim.mst_edges))

