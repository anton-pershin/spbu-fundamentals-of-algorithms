from pathlib import Path
from typing import Any, Union

import numpy as np
import networkx as nx

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class MatrixChainMultiplication:
    def __init__(self) -> None:

        self.counter = 0

    def run(
        self,
        matrices: list[dict[str, Union[str, tuple[int, int]]]]
    ) -> tuple[AnyNxGraph, Any]:

        n = len(matrices)

        names = [matrix["matrix_name"] for matrix in matrices]
        shapes = [matrix["shape"] for matrix in matrices]

        p = [shapes[0][0]]
        for shape in shapes:
            p.append(shape[1])

        dp = [[0 for _ in range(n)] for _ in range(n)]
        split = [[0 for _ in range(n)] for _ in range(n)]

        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                dp[i][j] = float("inf")

                for k in range(i, j):
                    cost = (
                        dp[i][k]
                        + dp[k + 1][j]
                        + p[i] * p[k + 1] * p[j + 1]
                    )

                    if cost < dp[i][j]:
                        dp[i][j] = cost
                        split[i][j] = k

        graph = nx.Graph()
        counter = 0

        def build_tree(i, j):
            nonlocal counter

            if i == j:
                graph.add_node(names[i])
                return names[i]

            root = f"node_{counter}"
            counter += 1

            graph.add_node(root)

            k = split[i][j]

            left = build_tree(i, k)
            right = build_tree(k + 1, j)

            graph.add_edge(root, left)
            graph.add_edge(root, right)

            return root

        root = build_tree(0, n - 1)

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

