from copy import copy
from pathlib import Path
from typing import Any

import numpy as np
import networkx as nx
from scipy.optimize import linprog

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph, NDArrayInt, NDArrayFloat


class ShortestPathLinearProgram:
    def __init__(self, G: AnyNxGraph) -> None:
        self.nodes: list(Any) = list[G.nodes]
        self.adj_matrix: NDArrayInt | NDArrayFloat = nx.adjacency_matrix(G).todense()

    def solve(self, s_node: Any, t_node: Any) -> set[tuple[Any, Any]]:
        edge_mask = self.adj_matrix != 0
        c = self.adj_matrix[edge_mask]
        A_eq = np.zeros(shape = (len(self.nodes) - 1, self.adj_matrix[edge_mask].shape[0]))


if __name__ == "__main__":
    G = nx.read_edgelist(Path("practicum_4") / "simple_weighted_graph_9_nodes.edgelist", create_using=nx.Graph)
    plot_graph(G)

    s_node = "0"
    t_node = "5"

    lp = ShortestPathLinearProgram(G)
    shortest_path_edges = lp.solve(s_node=s_node, t_node=t_node)
    plot_graph(G, highlighted_edges=shortest_path_edges)
