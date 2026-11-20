import sys
from pathlib import Path
from typing import Any, Union

import numpy as np
import networkx as nx

if __name__ == "__main__" and not __package__:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class MatrixChainMultiplication:
    def __init__(self) -> None:
        self.min_cost: Union[int, float] = 0

    def run(
        self,
        matrices: list[dict[str, Union[str, tuple[int, int]]]]
    ) -> tuple[AnyNxGraph, Any]:
        n = len(matrices)
        names = [m["matrix_name"] for m in matrices]
        dims = [matrices[0]["shape"][0]] + [m["shape"][1] for m in matrices]
        for i in range(n - 1):
            assert matrices[i]["shape"][1] == matrices[i + 1]["shape"][0], \
                f"Matrices {names[i]} and {names[i + 1]} cannot be multiplied"

        cost = [[0] * n for _ in range(n)]
        split = [[0] * n for _ in range(n)]
        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                cost[i][j] = np.inf
                for k in range(i, j):
                    c = cost[i][k] + cost[k + 1][j] + dims[i] * dims[k + 1] * dims[j + 1]
                    if c < cost[i][j]:
                        cost[i][j] = c
                        split[i][j] = k
        self.min_cost = cost[0][n - 1]

        tree = nx.Graph()
        counter = [0]

        def build(i: int, j: int) -> Any:
            if i == j:
                tree.add_node(names[i])
                return names[i]
            k = split[i][j]
            left = build(i, k)
            right = build(k + 1, j)
            node = f"({i}-{j})#{counter[0]}"
            counter[0] += 1
            tree.add_edge(node, left)
            tree.add_edge(node, right)
            return node

        root = build(0, n - 1)
        return tree, root


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

