from pathlib import Path
from typing import Any, Union

import numpy as np
import networkx as nx

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class MatrixChainMultiplication:
    def __init__(self) -> None:
        self._node_counter = 0
        self._split = None

    def _next_node_id(self) -> str:
        self._node_counter += 1
        return f"op_{self._node_counter}"

    def _build_tree(
        self,
        graph: nx.DiGraph,
        i: int,
        j: int,
        matrix_names: list[str]
    ) -> str:
        if i == j:
            node_id = matrix_names[i]
            graph.add_node(node_id)
            return node_id

        k = self._split[i][j]

        left_root = self._build_tree(graph, i, k, matrix_names)
        right_root = self._build_tree(graph, k + 1, j, matrix_names)

        internal_node = self._next_node_id()
        graph.add_node(internal_node)
        graph.add_edge(internal_node, left_root)
        graph.add_edge(internal_node, right_root)

        return internal_node

    def run(
        self,
        matrices: list[dict[str, Union[str, tuple[int, int]]]]
    ) -> tuple[AnyNxGraph, Any]:
        n = len(matrices)

        matrix_names = [m["matrix_name"] for m in matrices]

        dims = []
        for i, m in enumerate(matrices):
            rows, cols = m["shape"]
            if i == 0:
                dims.append(rows)
            dims.append(cols)

        dp = [[0] * n for _ in range(n)]
        self._split = [[-1] * n for _ in range(n)]

        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                dp[i][j] = float("inf")
                for k in range(i, j):
                    cost = dp[i][k] + dp[k + 1][j] + dims[i] * dims[k + 1] * dims[j + 1]
                    if cost < dp[i][j]:
                        dp[i][j] = cost
                        self._split[i][j] = k

        graph = nx.DiGraph()
        root = self._build_tree(graph, 0, n - 1, matrix_names)
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

