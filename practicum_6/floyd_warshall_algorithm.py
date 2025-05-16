from pathlib import Path
from typing import Any

import networkx as nx
import numpy as np

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class FloydWarshallAlgorithm:
    """
    This algorithm finds the shortest paths for all the node pairs
    """ 
    def __init__(self, G: nx.DiGraph) -> None:
        self.G = nx.DiGraph = G
        self.dist: dict[tuple[Any, Any], int] = {}
        self.shortest_paths: dict[tuple[Any, Any], set[tuple[Any, Any]]] = {}

    def run(self, node: Any) -> None:
        for n_1 in self.G.nodes():
            for n_2 in self.G.nodes():
                if (n_1, n_2) in G.edges:
                    self.dist[(n_1, n_2)] = G.edges[n_1, n_2]["weight"]
                    self.shortest_paths[(n_1, n_2)] = {(n_1, n_2)}
                else:
                    self.dist[(n_1, n_2)] = np.inf
                    self.shortest_paths[(n_1, n_2)] = set()

        for n_k in self.G.nodes():
            for n_i in self.G.nodes():
                for n_j in self.G.nodes():
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

