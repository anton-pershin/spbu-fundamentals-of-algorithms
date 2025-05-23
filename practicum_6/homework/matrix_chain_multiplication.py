from pathlib import Path
from typing import Any, Union

import numpy as np
import networkx as nx

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class MatrixChainMultiplication:
    def __init__(self) -> None:
        self.dp = None
        self.split = None
        self.node_counter = 0

    def _build_tree(self, matrices: list, i: int, j: int, G: nx.Graph) -> str:
        if i == j:
            return matrices[i]["matrix_name"]

        node_id = f"M{self.node_counter}"
        self.node_counter += 1

        k = self.split[i][j]
        left_child = self._build_tree(matrices, i, k, G)
        right_child = self._build_tree(matrices, k + 1, j, G)

        G.add_node(node_id)
        G.add_edge(node_id, left_child)
        G.add_edge(node_id, right_child)

        return node_id

    def run(
            self,
            matrices: list[dict[str, Union[str, tuple[int, int]]]]
    ) -> tuple[AnyNxGraph, Any]:
        n = len(matrices)
        if n == 0:
            return nx.Graph(), None

        self.dp = [[0] * n for _ in range(n)]
        self.split = [[0] * n for _ in range(n)]

        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                self.dp[i][j] = float('inf')
                for k in range(i, j):
                    cost = self.dp[i][k] + self.dp[k + 1][j] + matrices[i]["shape"][0] * matrices[k]["shape"][1] * matrices[j]["shape"][1]
                    if cost < self.dp[i][j]:
                        self.dp[i][j] = cost
                        self.split[i][j] = k

        G = nx.Graph()
        for matrix in matrices:
            G.add_node(matrix["matrix_name"])

        root = self._build_tree(matrices, 0, n - 1, G)
        return G, root


if __name__ == "__main__":
    test_matrices = [
        {"matrix_name": "A", "shape": (2, 3)},
        {"matrix_name": "B", "shape": (3, 10)},
        {"matrix_name": "C", "shape": (10, 20)},
        {"matrix_name": "D", "shape": (20, 3)},
    ]

    mcm = MatrixChainMultiplication()
    matmul_tree, root = mcm.run(test_matrices)
    plot_graph(matmul_tree)