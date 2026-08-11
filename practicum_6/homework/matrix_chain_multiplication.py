from pathlib import Path
from typing import Any, Union

import numpy as np
import networkx as nx

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class MatrixChainMultiplication:
    def __init__(self) -> None:
        self.G = nx.Graph()

    def run(
        self,
        matrices: list[dict[str, Union[str, tuple[int, int]]]]
    ) -> tuple[AnyNxGraph, Any]:

        DIM = len(matrices)
        M_SIZES = [matrices[0]["shape"][0]] + [matrix["shape"][1] for matrix in matrices]
        path_matrix = np.full((DIM, DIM), np.inf)
        k_matrix = np.zeros((DIM, DIM), dtype=int)

        for i in range(DIM):
            path_matrix[i, i] = 0

        for i in range(1, DIM):
            for j in range(0, DIM - i):
                for k in range(j, i + j):
                    possible_min_dist = path_matrix[j, k] + path_matrix[k + 1, i + j] + M_SIZES[j] * M_SIZES[k + 1] * M_SIZES[i + j + 1]
                    if possible_min_dist < path_matrix[j, i + j]:
                        path_matrix[j, i + j] = possible_min_dist
                        k_matrix[j, i + j] = k

        root = self.make_tree(k_matrix, matrices, 0, DIM - 1)
        return self.G, root

    def make_tree(self, dev_matrix: np.matrix, matrices: list[dict[str, Union[str, tuple[int, int]]]], start:int, end:int) -> AnyNxGraph:
        if start == end:
            self.G.add_node(matrices[start]["matrix_name"])
            return matrices[start]["matrix_name"]

        k = int(dev_matrix[start, end])
        left_child = self.make_tree(dev_matrix, matrices, start, k)
        right_child = self.make_tree(dev_matrix, matrices, k + 1, end)

        parent_name = " " * start + " " * end
        self.G.add_node(parent_name, label="")
        self.G.add_edge(parent_name, left_child)
        self.G.add_edge(parent_name, right_child)

        return parent_name



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

