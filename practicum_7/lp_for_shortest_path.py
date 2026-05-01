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
        self.nodes: list[Any] = list(G.node)
        self.adj_matrix : NDArrayInt | NDArrayFloat = nx.adjacency_matrix(G).todence()

    def solve(self, s_node: Any, t_node: Any) -> set[tuple[Any, Any]]:

        n_nodes = len(self.nodes)
        s_i = self.nodes.index(s_node)
        t_i = self.nodes.index(t_node)

        # Заполнить вектор C
        
        edge_mask = self.adj_matrix != 0
        c = self.adj_matrix[edge_mask]

        # Заполнить матрицу A_eq, shape = (n_nodes - 1,n_edges)
        
        A_eq = np.zeros(n_nodes, len(c),dtype=np.int_)
        node_indices = list(range(n_nodes))
        for i in range(n_nodes):
            rowcol_selector = copy(node_indices)
            rowcol_selector.remove(i)
            temp = self.adj_matrix.copy()
            temp[i,:][temp[i,:] != 0] = -1
            temp[:,i][temp[:,i] != 0] = 1
            temp[np.ix_(rowcol_selector,rowcol_selector)] = 0
            A_eq[i] = temp[edge_mask]

        rowcol_selector = copy(node_indices)
        rowcol_selector.remove(s_i)
        A_eq = A_eq[rowcol_selector]

        # Заполнить вектор b_eq
        
        b_eq = np.zeros((n_nodes,))
        b_eq[t_i] = 1
        b_eq = b_eq[rowcoll_selector]


        #  Решить линейную программу

        res = linprog(c, A_ub=None,b_ub=None,A_eq=A_eq,b_eq=b_eq,bounds=(0,None))

        #Возвратить множество ребер составляющих кратчайший путь

        ##########################
        ### PUT YOUR CODE HERE ###
        ##########################

        pass


if __name__ == "__main__":
    G = nx.read_edgelist(Path("practicum_4") / "simple_weighted_graph_9_nodes.edgelist", create_using=nx.Graph)
    plot_graph(G)

    s_node = "0"
    t_node = "5"

    lp = ShortestPathLinearProgram(G)
    shortest_path_edges = lp.solve(s_node=s_node, t_node=t_node)
    plot_graph(G, highlighted_edges=shortest_path_edges)
