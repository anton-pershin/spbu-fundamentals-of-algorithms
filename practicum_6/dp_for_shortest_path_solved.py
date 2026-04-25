from pathlib import Path
import heapq
from typing import Any
from collections import defaultdict

import networkx as nx
import numpy as np

from practicum_4.dfs_solved import TopologicalSorting
from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class DpAlgorithmForShortestPath:
    """
    Shortest path algorithm for directed acyclic graphs.
    """ 
    def __init__(self, G: nx.DiGraph) -> None:
        self.G: nx.DiGraph = G
        self.topo_sorting = TopologicalSorting(G)
        self.dist: dict[Any, int] = {}
        self.shortest_paths: dict[Any, set[tuple[Any, Any]]] = {}

    def run(self, node: Any) -> None:
        # Perform topological sorting
        sorted_nodes = self.topo_sorting.sort(node)
        self.dist[node] = 0
        self.shortest_paths[node] = set()
        for cur_node in sorted_nodes[1:]:  # skip the initial node
            # Find the shortest path to the current node
            predecessor_node = None
            min_path_weight = np.inf
            for n_neigh in self.G.predecessors(cur_node):
                path_weight = self.dist[n_neigh] + self.G.edges[n_neigh, cur_node]["weight"]
                if path_weight < min_path_weight:
                    predecessor_node = n_neigh
                    min_path_weight = path_weight

            # Update the distance and shortest paths since the current node
            # will never be visited again
            self.dist[cur_node] = min_path_weight
            self.shortest_paths[cur_node] = self.shortest_paths[predecessor_node] | {(predecessor_node, cur_node)}


class DpAlgorithmForShortestReliablePath:
    """
    Shortest path algorithm for directed acyclic graphs with additional
    constraint: the path cannot contain more than k edges
    """ 
    def __init__(self, G: nx.DiGraph, k: int) -> None:
        self.G: nx.DiGraph = G
        self.k: int = k
        self.topo_sorting = TopologicalSorting(G)
        self.dist: dict[(Any, Any), list[int]] = defaultdict(lambda: [np.inf] * (k + 1))
        self.shortest_paths: dict[(Any, Any), list[set[tuple[Any, Any]]]] = defaultdict(lambda: [set()] * (k + 1))

    def run(self, node: Any) -> None:
        # Perform topological sorting
        sorted_nodes = self.topo_sorting.sort(node)
        self.dist[node][0] = 0
        self.shortest_paths[node][0] = set()
        for node in sorted_nodes[1:]:  # skip the initial node
            # Find the shortest path to the current node
            for i in range(1, self.k + 1):
                predecessor_node = None
                min_path_weight = np.inf
                for n_neigh in self.G.predecessors(node):
                    path_weight = self.dist[n_neigh][i-1] + self.G.edges[n_neigh, node]["weight"]
                    if path_weight < min_path_weight:
                        predecessor_node = n_neigh
                        min_path_weight = path_weight

                # Update the distance and shortest paths since the current node
                # will never be visited again
                self.dist[node][i] = self.dist[predecessor_node][i-1] + min_path_weight
                self.shortest_paths[node][i] = self.shortest_paths[predecessor_node][i-1] | {(predecessor_node, node)}

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

