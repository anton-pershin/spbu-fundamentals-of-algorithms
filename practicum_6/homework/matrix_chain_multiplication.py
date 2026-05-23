from pathlib import Path
from typing import Any, Union

import numpy as np
import networkx as nx

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class MatrixChainMultiplication:
    def __init__(self) -> None:
        self.graph = nx.Graph()
        self.id = 0
 
    def new_node_id(self) -> int:
        node_id = self.id
        self.id += 1
        return node_id

    def run(
        self,
        matrices: list[dict[str, Union[str, tuple[int, int]]]]
    ) -> tuple[AnyNxGraph, Any]:

        n = len(matrices)
        names = [m["matrix_name"] for m in matrices]
        dims = [m["shape"][0] for m in matrices] + [matrices[-1]["shape"][1]]
 
        dp = [[0] * n for _ in range(n)]
        split = [[0] * n for _ in range(n)]
 
        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                dp[i][j] = float("inf")
                for k in range(i, j):
                    cost = (dp[i][k] + dp[k + 1][j]
                            + dims[i] * dims[k + 1] * dims[j + 1])
                    if cost < dp[i][j]:
                        dp[i][j] = cost
                        split[i][j] = k
 
        self.graph = nx.Graph()
        self.id = 0
 
        for name in names:
            self.graph.add_node(name)
 
        def build_tree(i: int, j: int) -> Any:
            if i == j:
                return names[i]
 
            k = split[i][j]
            left_child = build_tree(i, k)
            right_child = build_tree(k + 1, j)
 
            node_id = self.new_node_id()
            self.graph.add_node(node_id)
            self.graph.add_edge(node_id, left_child)
            self.graph.add_edge(node_id, right_child)
            return node_id
 
        root = build_tree(0, n - 1)
 
        return self.graph, root



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

