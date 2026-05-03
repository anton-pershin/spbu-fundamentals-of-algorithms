from pathlib import Path
from typing import Any, Union

import numpy as np
import networkx as nx

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph

    
class MatrixChainMultiplication:
    def __init__(self) -> None:

        self.G = nx.DiGraph()
        self.node_counter = 0


    def _get_new_node_id(self) -> str:
        self.node_counter += 1
        return f"op_{self.node_counter}"
    

    def _build_tree(self, i: int, j: int, split: list, names: list) -> tuple[str, AnyNxGraph]:
        if i == j:
            node_name = names[i]
            self.G.add_node(node_name, label=node_name)
            return node_name, self.G
        
        k = split[i][j]
        left_id, _ = self._build_tree(i, k, split, names)
        right_id, _ = self._build_tree(k + 1, j, split, names)

        internal_id = self._get_new_node_id()
        self.G.add_node(internal_id, label=f"({left_id} * {right_id})")
        self.G.add_edge(internal_id, left_id)
        self.G.add_edge(internal_id, right_id)

        return internal_id, self.G



    def run(
        self,
        matrices: list[dict[str, Union[str, tuple[int, int]]]]
    ) -> tuple[AnyNxGraph, Any]:
        
        self.G = nx.DiGraph()
        self.node_counter = 0
        
        n = len(matrices)

        names = [m["matrix_name"] for m in matrices]
        shapes = [m["shape"] for m in matrices]

        if n == 1:
            root = names[0]
            self.G.add_node(root, label=root)
            return self.G, root
        
        p = []
        for i, (rows, cols) in enumerate(shapes):
            if i == 0:
                p.append(rows)
            p.append(cols)

        INF = float('inf')
        dp = [[0] * n for _ in range(n)]
        split = [[0] * n for _ in range(n)]

        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                dp[i][j] = INF
                for k in range(i, j):
                    cost = dp[i][k] + dp[k + 1][j] + p[i] * p[k + 1] * p[j + 1]
                    if cost < dp[i][j]:
                        dp[i][j] = cost
                        split[i][j] = k

        root, self.G = self._build_tree(0, n - 1, split, names)

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

