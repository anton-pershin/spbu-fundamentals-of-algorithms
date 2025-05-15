from pathlib import Path
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

        self.dist[node] = 0
        self.shortest_paths[node] = set()

        sorted_nodes = self.topo_sorting.sort(node)
        for cur_node in sorted_nodes[1:]:
            predecessot_node = None
            min_path_weight = np.inf
            for n_neigh in self.G.predecessors(cur_node):
                path_weight = self.dist[n_neigh] + self.G.edges[n_neigh, cur_node]["weight"]
                if path_weight < min_path_weight:
                    min_path_weight = path_weight
                    predecessot_node = n_neigh
            
            self.dist[cur_node] = min_path_weight
            self.shortest_paths[cur_node] = self.shortest_paths[predecessot_node] | {(predecessot_node, cur_node)}
            



        

            

class DpAlgorithmForShortestReliablePath:
    """
    Shortest path algorithm for directed acyclic graphs with additional
    constraint: the path cannot contain more than k edges
    """ 
    def __init__(self, G: nx.DiGraph, k: int) -> None:

        self.k: int = k
        self.G: nx.DiGraph = G
        self.topo_sorting = TopologicalSorting(G)
        self.dist: dict[Any, list[int]] = defaultdict(lambda: [np.inf] * (k + 1))
        self.shortest_paths: dict[Any, list[set[tuple[Any, Any]]]] = defaultdict(lambda: [set()] * (k + 1))

    def run(self, node: Any) -> None:

        self.dist[node][0] = [0]
        self.shortest_paths[node][0] = set()

        sorted_nodes = self.topo_sorting.sort(node)

        for i in range(1, self.k+1):

            for cur_node in sorted_nodes[1:]:
                predecessot_node = None
                min_path_weight = np.inf
                for n_neigh in self.G.predecessors(cur_node):
                    path_weight = self.dist[n_neigh][i-1] + self.G.edges[n_neigh, cur_node]["weight"]
                    if path_weight < min_path_weight:
                        min_path_weight = path_weight
                        predecessot_node = n_neigh
                
                self.dist[cur_node][i] = min_path_weight
                self.shortest_paths[cur_node][i] = self.shortest_paths[predecessot_node][i-1] | {(predecessot_node, cur_node)}
            


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

