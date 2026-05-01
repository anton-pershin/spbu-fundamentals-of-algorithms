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

        dims = []
        for i, m in enumerate(matrices):
            r, c = m["shape"]
            if i == 0:
                dims.append(r)
            dims.append(c)

        dp = [[0] * n for _ in range(n)]
        split = [[None] * n for _ in range(n)]

        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                dp[i][j] = float("inf")

                for k in range(i, j):
                    cost = (
                        dp[i][k]
                        + dp[k + 1][j]
                        + dims[i] * dims[k + 1] * dims[j + 1]
                    )

                    if cost < dp[i][j]:
                        dp[i][j] = cost
                        split[i][j] = k

        G = nx.DiGraph()
        node_id_counter = [0]

        def new_node():
            node_id_counter[0] += 1
            return f"v{node_id_counter[0]}"

        leaves = []
        for m in matrices:
            name = m["matrix_name"]
            G.add_node(name, type="matrix", shape=m["shape"])
            leaves.append(name)

        def build(i: int, j: int):
            if i == j:
                return matrices[i]["matrix_name"]

            k = split[i][j]

            left = build(i, k)
            right = build(k + 1, j)

            node = new_node()
            G.add_node(node, type="mul")

            G.add_edge(node, left)
            G.add_edge(node, right)

            return node

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

