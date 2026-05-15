from pathlib import Path
import heapq
from typing import Any
from functools import reduce

import networkx as nx
import numpy as np

from practicum_4.dfs_solved import TopologicalSorting
from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class FloydWarshallAlgorithm:
    """
    This algorithm finds the shortest paths for all the node pairs
    """ 
    def __init__(self, G: nx.DiGraph) -> None:
        self.G: nx.DiGraph = G
        self.dist: dict[(Any, Any), int] = {}
        self.shortest_paths: dict[(Any, Any), set[tuple[Any, Any]]] = {}

    def run(self, node: Any) -> None:
        # Initialize distances and shortest paths
        for n_1 in self.G.nodes():
            for n_2 in self.G.nodes():
                self.dist[(n_1, n_2)] = np.inf
                self.shortest_paths[(n_1, n_2)] = set()

        # Define L0 shortest paths (connected nodes have edges as trivial paths)
        for n_start, n_end, data in self.G.edges(data=True):
            self.dist[(n_start, n_end)] = data["weight"]
            self.shortest_paths[(n_start, n_end)] = {(n_start, n_end)}

        # Starting from one-edge paths, we check two-edge paths etc.
        for n_k in self.G.nodes():
            for n_i in self.G.nodes():
                for n_j in self.G.nodes():
                    # Check whether the path from n_i to n_j via n_k is shorter
                    if self.dist[(n_i, n_j)] > self.dist[(n_i, n_k)] + self.dist[(n_k, n_j)]:
                        self.dist[(n_i, n_j)] = self.dist[(n_i, n_k)] + self.dist[(n_k, n_j)]
                        self.shortest_paths[(n_i, n_j)] = self.shortest_paths[(n_i, n_k)] | self.shortest_paths[(n_k, n_j)]


if __name__ == "__main__":
    G = nx.read_edgelist(
        Path("practicum_4") / "simple_weighted_graph_9_nodes.edgelist",
        create_using=nx.DiGraph
    )
    plot_graph(G)

    fw = FloydWarshallAlgorithm(G)
    fw.run(node="0")
    plot_graph(G, highlighted_edges=list(fw.shortest_paths[("0", "5")]))

