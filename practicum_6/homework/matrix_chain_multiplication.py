from pathlib import Path
from typing import Any, Union

import numpy as np
import networkx as nx

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class MatrixChainMultiplication:
    def __init__(self) -> None:

        self.node_count=0
        pass

    def build(self,l,r,matrices,sep):
        if l==r:
            node = matrices[l]["matrix_name"]
            self.G.add_node(node)
            return node
        k = sep[l][r]
        left = self.build(l, k, matrices, sep)
        right = self.build(k + 1, r, matrices, sep)
        node = self.node_count
        self.node_count += 1
        self.G.add_node(node)
        self.G.add_edge(node, left)
        self.G.add_edge(node, right)
        return node


    def run(
        self,
        matrices: list[dict[str, Union[str, tuple[int, int]]]]
    ) -> tuple[AnyNxGraph, Any]:

        n = len(matrices)
        size = []
        for m in matrices:
            size.append(m["shape"][0])
        size.append(matrices[-1]["shape"][1])
        dp = [[0] * n for i in range(n)]
        sep = [[-1] * n for i in range(n)]
        for step in range(1, n):
            for i in range(0, n - step):
                j = i + step
                dp[i][j] = float('inf')
                for k in range(i, j):
                    cost = dp[i][k] + dp[k + 1][j] + size[i] * size[k + 1] * size[j + 1]
                    if cost < dp[i][j]:
                        dp[i][j] = cost
                        sep[i][j] = k
        self.G = nx.Graph()
        self.node_count = 0
        root = self.build(0, n - 1, matrices, sep)

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
