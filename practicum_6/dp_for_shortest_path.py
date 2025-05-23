from pathlib import Path
from typing import Any
from collections import defaultdict
import networkx as nx
import numpy as np

from practicum_4.dfs import TopologicalSorting
from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class DpAlgorithmForShortestPath:
    """
    Shortest path algorithm for directed acyclic graphs.
    """ 
    def __init__(self, G: nx.DiGraph) -> None:
        self.G: nx.DiGraph = G
        self.topo_sorting = TopologicalSorting(G)
        self.dist: dict[Any, int] = {n: -1 for n in G.nodes}
        self.shortest_paths: dict[Any, set[tuple[Any, Any]]] = {}

    def run(self, node: Any) -> None:

        self.dist[node] = 0
        self.shortest_paths[node] = set()
        sorted_nodes = self.topo_sorting.sort(node)

        for curr in sorted_nodes[1:]:
            pred_node = None
            min_path_weight = np.inf
            for n_neigh in self.G.predecessors(curr):
                path_weight = self.dist[n_neigh] + self.G.edges[n_neigh, curr]["weight"]
                if path_weight < min_path_weight:
                    min_path_weight = path_weight
                    pred_node = n_neigh
            self.dist[curr] = min_path_weight
            self.shortest_paths[curr] = self.shortest_paths[pred_node] | {(pred_node, curr)}


class DpAlgorithmForShortestReliablePath:
    """
    Shortest path algorithm for directed acyclic graphs with additional
    constraint: the path cannot contain more than k edges
    """ 
    def __init__(self, G: nx.DiGraph, k: int) -> None:
        self.G: nx.DiGraph = G
        self.k: int = k
        self.topo_sorting = TopologicalSorting(G)
        self.dist: dict[Any, list[int]] = defaultdict(lambda: [np.inf] * (self.k+1))
        self.shortest_paths: dict[Any, list[set[tuple[Any, Any]]]] = defaultdict(lambda: [set()] * (self.k+1))

    def run(self, node: Any) -> None:
        self.dist[node][0] = 0
        self.shortest_paths[node][0] = set()
        sorted_nodes = self.topo_sorting.sort(node)
        for i in range(1, self.k + 1):
            for curr in sorted_nodes[1:]:
                pred_node = None
                min_path_weight = np.inf
                for n_neigh in self.G.predecessors(curr):
                    path_weight = self.dist[n_neigh][i-1] + self.G.edges[n_neigh, curr]["weight"]
                    if path_weight < min_path_weight and path_weight <= self.k:
                        min_path_weight = path_weight
                        pred_node = n_neigh
                self.dist[curr][i] = min_path_weight
                self.shortest_paths[curr][i] = self.shortest_paths[pred_node][i-1] | {(pred_node, curr)}
        


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

    # dp = DpAlgorithmForShortestReliablePath(G, k=3)
    # dp.run(node="0")
    # plot_graph(G, highlighted_edges=list(dp.shortest_paths["5"][2]))
    # plot_graph(G, highlighted_edges=list(dp.shortest_paths["5"][3]))

