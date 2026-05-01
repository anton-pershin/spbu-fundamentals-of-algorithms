from pathlib import Path
from typing import Any, Union

import numpy as np
import networkx as nx

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class MatrixChainMultiplication:
    def __init__(self) -> None:
        self.smallest_multiplication = None
        self.order_to_multiplication = None
        self.graph = None
        self.root_id = None


    def run(self, matrices: list[dict[str, Union[str, tuple[int, int]]]]) -> tuple[AnyNxGraph, Any]:
        n = len(matrices)
        self.smallest_multiplication = np.zeros((n, n))
        self.order_to_multiplication = np.zeros((n, n))
        columns = [matrices[0]["shape"][0]] + [mat["shape"][1] for mat in matrices]

        len_step = 2
        while len_step <= n:
            for i in range(0, n-len_step + 1):
                min_i_len = np.inf
                j = i + len_step - 1
                for k in range(i, j):
                    if min_i_len > self.smallest_multiplication[i][k] + self.smallest_multiplication[k+1][j] + columns[i] * columns[k + 1] * columns[j + 1]:
                        min_i_len = self.smallest_multiplication[i][k] + self.smallest_multiplication[k+1][j] + columns[i] * columns[k + 1] * columns[j + 1]
                        self.order_to_multiplication[i][j] = k
                self.smallest_multiplication[i][j] = min_i_len
            len_step += 1

        self.graph = nx.Graph()

        if n == 0:
            self.root_id = None
            return self.graph, self.root_id

        node_counter = 0

        def build_bin_tree(i: int, j: int) -> AnyNxGraph:
            nonlocal node_counter
            if i == j:
                node_name = matrices[i]["matrix_name"]
                self.graph.add_node(node_name)
                return node_name

            k = int(self.order_to_multiplication[i][j])
            left = build_bin_tree(i, k)
            right = build_bin_tree(k + 1, j)
            inner_node = f"inner_{node_counter}"
            node_counter += 1
            self.graph.add_node(inner_node)
            self.graph.add_edge(left, inner_node)
            self.graph.add_edge(right, inner_node)
            return inner_node
        root = build_bin_tree(0,n - 1)
        return self.graph, root



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

