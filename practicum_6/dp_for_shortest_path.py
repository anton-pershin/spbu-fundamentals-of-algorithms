from pathlib import Path
from typing import Any
from operator import itemgetter

import networkx as nx
import numpy as np



from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class DpAlgorithmForShortestPath:
    """
    Shortest path algorithm for directed acyclic graphs.
    """ 
    def __init__(self, G: nx.DiGraph) -> None:
        self.G: nx.DiGraph = G
        self.topo_sorting = To

    def run(self, node: Any) -> None:
        sorted_nodes = self.topo_sorting.sort(node)
        self.dist[node]= 0
        self.shortest_paths[node] = set()

        for cur in sorted_nodes[1:]:
            predecessors_node = None
            min_path_w = np.inf
            for v in G.predecessors(cur_node):
                path_w =  self.dist[v] +self.G.edges[v,cur_node]["w"]
                if path_w < min_path_w:
                    min_path_w= path_w
                    predecessors_node= v
            self.dist[cur_node] = min_path_w
            self.shortest_paths



                



class DpAlgorithmForShortestReliablePath:
    """
    Shortest path algorithm for directed acyclic graphs with additional
    constraint: the path cannot contain more than k edges
    """ 
    def __init__(self, G: nx.DiGraph, k: int) -> None:

        ...


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

