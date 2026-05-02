from pathlib import Path
from typing import Any
from operator import itemgetter

import networkx as nx
import numpy as np


from src.plotting.graphs import plot_graph
from practicum_4.dfs_solved import TopologicalSorting
from src.common import AnyNxGraph


class DpAlgorithmForShortestPath:
    """
    Shortest path algorithm for directed acyclic graphs.
    """ 
    def __init__(self, G: nx.DiGraph) -> None:

        self.G: nx.DiGraph = G
        self.topo_sorting: TopologicalSorting = TopologicalSorting(G)
        self.dist: dict[Any, int] = {}
        self.shortest_paths: dict[Any, set[tuple[Any, Any]]] = {}

    def run(self, node: Any) -> None:

        sorted_nodes = self.topo_sorting.sort(node)
        self.dist[node] = 0
        self.shortest_paths[node] = set()

        for cur_node in sorted_nodes[1:]:
            predecessors = list(self.G.predecessors(cur_node))
            paths = [self.dist[n_neigh] + self.G.edges[n_neigh, cur_node]["weight"] for n_neigh in predecessors]
            n_neigh, min_path = min(zip(predecessors, paths), key=itemgetter(1))
            self.dist[cur_node] = min_path
            self.shortest_paths[cur_node] = self.shortest_paths[n_neigh] | {(n_neigh, cur_node)}


class DpAlgorithmForShortestReliablePath:
    """
    Shortest path algorithm for directed acyclic graphs with additional
    constraint: the path cannot contain more than k edges
    """ 
    def __init__(self, G: nx.DiGraph, k: int) -> None:
        self.G: nx.DiGraph = G
        self.dist: dict[(Any, Any), int] = {}
        self.shortest_paths: dict[(Any, Any), set[tuple[Any, Any]]] = {}

    def run(self, node: Any) -> None:
        


if __name__ == "__main__":
    G = nx.read_edgelist(
        Path("practicum_6") / "simple_weighted_graph_9_nodes.edgelist",
        create_using=nx.DiGraph
    )
    plot_graph(G)

    # Run DP algorithm for shortest path
    dp = DpAlgorithmForShortestPath(G)
    dp.run(node="0")
    plot_graph(G, highlighted_edges=list(dp.shortest_paths["5"]))

    # Run DP algorithm for the shortest reliable path
    # (at most 3 edges)
    dp = DpAlgorithmForShortestReliablePath(G, k=3)
    dp.run(node="0")
    plot_graph(G, highlighted_edges=list(dp.shortest_paths["5"][2]))
    plot_graph(G, highlighted_edges=list(dp.shortest_paths["5"][3]))

