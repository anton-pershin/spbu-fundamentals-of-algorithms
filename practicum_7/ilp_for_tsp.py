from pathlib import Path
from typing import Any

import numpy as np
import networkx as nx
from scipy.optimize import milp, Bounds, LinearConstraint

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph, NDArrayInt, NDArrayFloat


class TSPIntegerLinearProgram:
    def __init__(self, G: AnyNxGraph) -> None:

        ##########################
        ### PUT YOUR CODE HERE ###
        ##########################

        pass

    def solve(self, start_node: Any) -> set[tuple[Any, Any]]:

        ##########################
        ### PUT YOUR CODE HERE ###
        ##########################

        pass

    @staticmethod
    def build_edge_idx_map(adj_matrix: NDArrayInt | NDArrayFloat) -> dict[tuple[int, int], int]:
        edge_idx_map = {}
        edge_idx = 0
        for i in range(adj_matrix.shape[0]):
            for j in range(adj_matrix.shape[1]):
                if adj_matrix[i, j] != 0:
                    edge_idx_map[(i, j)] = edge_idx
                    edge_idx += 1
        return edge_idx_map


if __name__ == "__main__":
    G = nx.complete_graph(5, create_using=nx.DiGraph)
    for u, v in G.edges():
        G.edges[u, v]["weight"] = np.random.randint(1, 20)
    plot_graph(G)

    start_node = 0
    ilp = TSPIntegerLinearProgram(G)
    tour_edges = ilp.solve(start_node=start_node)
    plot_graph(G, highlighted_edges=list(tour_edges))
