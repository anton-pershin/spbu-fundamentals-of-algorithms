from pathlib import Path
from typing import Any, Union

import numpy as np
import networkx as nx

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class MatrixChainMultiplication:
    def __init__(self) -> None:
        self.node_counter = 0

    def run(
            self,
            matrices: list[dict[str, Union[str, tuple[int, int]]]]
    ) -> tuple[AnyNxGraph, Any]:

        m_count = len(matrices) # matrices count

        dim = list() # dimensions
        dim.append(matrices[0]["shape"][0])
        for m in matrices:
            dim.append(m["shape"][1])

        costs = np.zeros((m_count, m_count))
        splits = np.zeros((m_count, m_count), dtype=int)

        for L in range(2, m_count + 1): # length
            for l in range(m_count - L + 1): # left
                r = l + L - 1 # right
                costs[l][r] = float('inf')
                for s in range(l, r): # split
                    c = costs[l][s] + costs[s + 1][r] + dim[l] * dim[s + 1] * dim[r + 1] # cost
                    if c < costs[l][r]:
                        costs[l][r] = c
                        splits[l][r] = s

        graph = nx.Graph()
        self.node_counter = 0

        def build_tree(l, r):
            if l == r:
                leaf_name = matrices[l]["matrix_name"]
                graph.add_node(leaf_name)
                return leaf_name

            current_node = f"{self.node_counter}"
            self.node_counter += 1
            graph.add_node(current_node)

            s_p = splits[l][r] # split point
            left_child = build_tree(l, s_p)
            right_child = build_tree(s_p + 1, r)

            graph.add_edge(current_node, left_child)
            graph.add_edge(current_node, right_child)

            return current_node

        root = build_tree(0, m_count - 1)
        return graph, root

if __name__ == "__main__":

    test_matrices = [
        {
            "matrix_name": "A",
            "shape": (2, 3),
        },
        {
            "matrix_name": "B",
            "shape": (3, 10),
        },
        {
            "matrix_name": "C",
            "shape": (10, 20),
        },
        {
            "matrix_name": "D",
            "shape": (20, 3),
        },
    ]

    mcm = MatrixChainMultiplication()
    matmul_tree, root = mcm.run(test_matrices)

    plot_graph(matmul_tree)

