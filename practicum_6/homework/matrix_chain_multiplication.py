from pathlib import Path
from typing import Any, Union

import numpy as np
import networkx as nx

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class MatrixChainMultiplication:
    def __init__(self) -> None:
        pass

    def run(
        self,
        matrices: list[dict[str, Union[str, tuple[int, int]]]]
    ) -> tuple[AnyNxGraph, Any]:
        n = len(matrices)
        names = [m["matrix_name"] for m in matrices]
        shapes = [m["shape"] for m in matrices]

        # p[0] = число строк первой матрицы, p[i] = число столбцов i-й матрицы
        p = [shapes[0][0]] + [shapes[i][1] for i in range(n)]

        cost = [[0] * n for _ in range(n)]
        split = [[0] * n for _ in range(n)]

        for chain_len in range(2, n + 1):
            for i in range(n - chain_len + 1):
                j = i + chain_len - 1
                cost[i][j] = float("inf")
                for k in range(i, j):
                    q = cost[i][k] + cost[k + 1][j] + p[i] * p[k + 1] * p[j + 1]
                    if q < cost[i][j]:
                        cost[i][j] = q
                        split[i][j] = k

        G = nx.Graph()
        self._internal_counter = 0

        def build(i: int, j: int) -> Any:
            if i == j:
                node_id = names[i]
                G.add_node(node_id)
                return node_id

            k = split[i][j]
            left = build(i, k)
            right = build(k + 1, j)

            node_id = f"P{self._internal_counter}"
            self._internal_counter += 1
            G.add_node(node_id)
            G.add_edge(node_id, left)
            G.add_edge(node_id, right)
            return node_id

        root = build(0, n - 1)
        return G, root


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
