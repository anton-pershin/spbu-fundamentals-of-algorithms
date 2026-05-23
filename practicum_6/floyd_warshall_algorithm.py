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

        self.G: nx.DiGraph = G
        self.dist: dict[(Any, Any), int] = {}
        self.shortest_paths: dict[(Any, Any), set[tuple[Any, Any]]] = {}

    def run(self, node: Any) -> None:

        for u in self.G.nodes():
            for v in self.G.nodes():
                if u == v:
                    self.dist[(u, v)] = 0
                    self.shortest_paths[(u, v)] = set()
                elif self.G.has_edge(u, v):
                    self.dist[(u, v)] = self.G.edges[u, v]['weight']
                    self.shortest_paths[(u, v)] = set([(u, v)])
                else:
                    self.dist[(u, v)] = float('inf')
                    self.shortest_paths[(u, v)] = set()

        for k in self.G.nodes():
            for i in self.G.nodes():
                for j in self.G.nodes():
                    if self.dist[(i, k)] + self.dist[(k, j)] < self.dist[(i, j)]:
                        self.dist[(i, j)] = self.dist[(i, k)] + self.dist[(k, j)]
                        self.shortest_paths[(i, j)] = self.shortest_paths[(i, k)] | self.shortest_paths[(k, j)]
                    elif self.dist[(i, k)] + self.dist[(k, j)] == self.dist[(i, j)]:
                        self.shortest_paths[(i, j)].update(self.shortest_paths[(i, k)])
                        self.shortest_paths[(i, j)].update(self.shortest_paths[(k, j)])



if __name__ == "__main__":
    G = nx.read_edgelist(
        Path("practicum_4") / "simple_weighted_graph_9_nodes.edgelist",
        create_using=nx.DiGraph
    )
    plot_graph(G)

    fw = FloydWarshallAlgorithm(G)
    fw.run(node="0")
    plot_graph(G, highlighted_edges=list(fw.shortest_paths[("0", "5")]))

