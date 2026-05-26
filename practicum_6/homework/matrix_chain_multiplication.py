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
        if n == 0:
            return nx.Graph(), None

        names = [m["matrix_name"] for m in matrices]
        rows = [m["shape"][0] for m in matrices]
        cols = [m["shape"][1] for m in matrices]

        m = [[0] * n for _ in range(n)]
        s = [[0] * n for _ in range(n)]

        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                m[i][j] = float("inf")
                for k in range(i, j):
                    cost = m[i][k] + m[k + 1][j] + rows[i] * cols[k] * cols[j]
                    if cost < m[i][j]:
                        m[i][j] = cost
                        s[i][j] = k

        G = nx.Graph()

        def build(i: int, j: int) -> Any:
            if i == j:
                node = names[i]
                G.add_node(node)
                return node
            k = s[i][j]
            left = build(i, k)
            right = build(k + 1, j)
            node = (i, j)
            G.add_node(node)
            G.add_edge(node, left)
            G.add_edge(node, right)
            return node

        if n == 1:
            root = names[0]
            G.add_node(root)
        else:
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