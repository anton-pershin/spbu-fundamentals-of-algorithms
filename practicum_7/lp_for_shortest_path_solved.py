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
        self.nodes: list[Any] = list(G.nodes)
        self.adj_matrix: NDArrayInt | NDArrayFloat = nx.adjacency_matrix(G).todense()

    def solve(self, s_node: Any, t_node: Any) -> set[tuple[Any, Any]]:
        n_nodes = len(self.nodes)
        s_i = self.nodes.index(s_node)
        t_i = self.nodes.index(t_node)

        # Form vector c as a vector of A_{ij} corresponding to non-zero entries
        # Thus, vector x will follow the same indices
        edge_mask = (
            self.adj_matrix != 0
        )  # this is a vector whose "True" values correspond to actual edges
        c = self.adj_matrix[edge_mask].reshape(-1)

        # Form A_eq, i.e. source, sink and conversation equations
        A_eq = np.zeros((n_nodes, len(c)), dtype=np.int_)
        node_indices = list(range(n_nodes))
        for i in range(n_nodes):
            rowcol_selector = copy(node_indices)
            rowcol_selector.remove(i)
            temp = self.adj_matrix.copy()
            temp[i, :][temp[i, :] != 0] = -1
            temp[:, i][temp[:, i] != 0] = 1
            temp[np.ix_(rowcol_selector, rowcol_selector)] = 0
            A_eq[i] = temp[edge_mask]  # a vector will be written here!

        # Remove source node from A_eq
        rowcol_selector = copy(node_indices)
        rowcol_selector.remove(s_i)
        A_eq = A_eq[rowcol_selector]

        # Form the RHS vector b. It is full of zeros
        # except for node t where it should be one
        # and node s which should not be present at all
        b_eq = np.zeros((n_nodes,), dtype=np.int_)
        b_eq[t_i] = 1
        b_eq = b_eq[rowcol_selector]

        # Solve the LP problem
        res = linprog(c, A_ub=None, b_ub=None, A_eq=A_eq, b_eq=b_eq, bounds=(0, None))

        # Prepare the plotting-friendly path
        edge_idx_to_adj_matrix_idx_map = self.build_edge_idx_to_adj_matrix_idx_map(self.adj_matrix)
        shortest_path_edges = set()
        for i, path_segment_value in enumerate(res.x):
            if path_segment_value != 0.0:
                in_idx, out_idx = edge_idx_to_adj_matrix_idx_map[i]
                shortest_path_edges.add((self.nodes[in_idx], self.nodes[out_idx]))
        return shortest_path_edges

    @staticmethod
    def build_edge_idx_to_adj_matrix_idx_map(adj_matrix: NDArrayInt | NDArrayFloat) -> dict[int, tuple[int, int]]:
        edge_idx_to_adj_matrix_idx = {}
        edge_idx = 0
        for i in range(adj_matrix.shape[0]):
            for j in range(adj_matrix.shape[1]):
                if adj_matrix[i, j] != 0:
                    edge_idx_to_adj_matrix_idx[edge_idx] = (i, j)
                    edge_idx += 1
        return edge_idx_to_adj_matrix_idx


if __name__ == "__main__":
    G = nx.read_edgelist(Path("practicum_4") / "simple_weighted_graph_9_nodes.edgelist", create_using=nx.Graph)
    plot_graph(G)

    s_node = "0"
    t_node = "5"

    lp = ShortestPathLinearProgram(G)
    shortest_path_edges = lp.solve(s_node=s_node, t_node=t_node)
    plot_graph(G, highlighted_edges=shortest_path_edges)
