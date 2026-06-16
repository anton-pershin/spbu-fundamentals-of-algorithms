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
        self.sizes = None
        self.G = nx.Graph()
        self.node_num = 0

    def build(self, l, r, names):
        if l == r - 1:
            node = names[l]
            self.G.add_node(node)
            return node

        i = self.split[l, r]

        left = self.build(l, i, names)
        right = self.build(i, r, names)

        self.node_num += 1
        parent = f"mul_{self.node_num}"
        self.G.add_node(parent)

        self.G.add_edge(parent, left)
        self.G.add_edge(parent, right)

        return parent

    def run(
        self,
        matrices: list[dict[str, Union[str, tuple[int, int]]]]
    ) -> tuple[AnyNxGraph, Any]:
        n = len(matrices)
        self.G = nx.Graph()
        self.node_num = 0

        if n == 0:
            return self.G, None

        names = [m["matrix_name"] for m in matrices]
        shapes = [m["shape"] for m in matrices]

        self.sizes = np.array([shapes[0][0]] + [s[1] for s in shapes], dtype=int)

        self.dp = np.full((n + 1, n + 1), np.inf)
        self.split = np.full((n + 1, n + 1), -1, dtype=int)

        for i in range(n):
            self.dp[i, i + 1] = 0

        for i in range(2, n + 1):
            for l in range(0, n - i + 1):
                r = l + i
                for k in range(l + 1, r):
                    curr = (self.dp[l, k] + self.dp[k, r] + self.sizes[l] * self.sizes[k] * self.sizes[r])

                    if curr < self.dp[l, r]:
                        self.dp[l, r] = curr
                        self.split[l, r] = k

        root = self.build(0, n, names)
        return self.G, root

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