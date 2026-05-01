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
        create_using=nx.DiGraph
    )
    plot_graph(G)

    fw = FloydWarshallAlgorithm(G)
    fw.run(node="0")
    plot_graph(G, highlighted_edges=list(fw.shortest_paths[("0", "5")]))

