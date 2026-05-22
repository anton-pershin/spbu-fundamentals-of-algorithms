from pathlib import Path
from typing import Any

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
        self.dist: dict[Any, int] = {}
        self.shortest_paths: dict[Any, set[tuple[Any, Any]]] = {}


    def run(self, node: Any) -> None:
        shorted_nodes = self.topo_sorting.sort(node)
        self.dist[node] = 0
        self.shortest_paths[node] = set()

        for cur_node in shorted_nodes[1:]:
            predessesor_node = None
            min_path_weight = np.inf

            for n_neigh in self.G.predecessors(cur_node):
                path_weight = self.dist[n_neigh] + self.G.edges[n_neigh, cur_node]["weight"]
                if path_weight < min_path_weight:
                    min_path_weight = path_weight
                    predessesor_node = n_neigh
            
            self.dist[cur_node] = min_path_weight
            self.shortest_paths[cur_node] = self.shortest_paths[predessesor_node] | {(predessesor_node, cur_node)}
        
            


class DpAlgorithmForShortestReliablePath:
    """
    Shortest path algorithm for directed acyclic graphs with additional
    constraint: the path cannot contain more than k edges
    """ 
    def __init__(self, G: nx.DiGraph, k: int) -> None:

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

