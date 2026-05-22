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
        # заполнить c
        edge_mask = self.adj_matrix != 0
        c = self.adj_matrix[edge_mask]

        # заполнить A_eq, shape = (n_nodes - 1, n_edges)
        A_eq = np.zeros((n_nodes, len(c)), dtype=np.int_)
        node_indices = list(range(n_nodes))
        for i in range(n_nodes):
            rowcol_selector = copy(node_indices)
            rowcol_selector.remove(i)
            temp = self.adj_matrix.copy()
            temp[i, :][temp[i, :] != 0] = -1
            temp[:, i][temp[:, i] != 0] = 1
            temp[np.ix_(rowcol_selector, rowcol_selector)] = 0
            A_eq[i] = temp[edge_mask]
        rowcol_selector = copy(node_indices)
        rowcol_selector.remove(s_i)
        A_eq = A_eq[rowcol_selector]

        # заполнить b_eq
        b_eq = np.zeros((n_nodes,))
        b_eq[t_i] = 1
        b_eq = b_eq[rowcol_selector]

        # решить линейную программу
        res = linprog(c, A_ub=None, b_ub=None, A_eq=A_eq, b_eq=b_eq, bounds=(0, None))
        breakpoint()
        # возвратить множество ребер, составляющих кратчайший путь


if __name__ == "__main__":
    G = nx.read_edgelist(Path("practicum_4") / "simple_weighted_graph_9_nodes.edgelist", create_using=nx.Graph)
    plot_graph(G)

    s_node = "0"
    t_node = "5"

    lp = ShortestPathLinearProgram(G)
    shortest_path_edges = lp.solve(s_node=s_node, t_node=t_node)
    plot_graph(G, highlighted_edges=shortest_path_edges)
