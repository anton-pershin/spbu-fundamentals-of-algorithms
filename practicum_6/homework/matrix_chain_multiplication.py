from pathlib import Path
from typing import Any, Union

import numpy as np
import networkx as nx

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph

class MatrixChainMultiplication:
    def __init__(self) -> None:
        
        self.graph = nx.Graph()
        self.matrices = []
        self.n = 0
        self.dimensions = []
        self.dp = []
        self.splits = []

    def run(
        self,
        matrices: list[dict[str, Union[str, tuple[int, int]]]]
    ) -> tuple[AnyNxGraph, Any]:
        
        self.matrices = matrices
        self.n = len(self.matrices)

        self.dimensions = [self.matrices[i]['shape'][0] for i in range(self.n)] + [self.matrices[-1]['shape'][1]]

        self.dp = [[0] * self.n for _ in range(self.n)]
        self.splits = [[0] * self.n for _ in range(self.n)]

        for length in range(2, self.n + 1):
            for i in range(self.n - length + 1):
                j = i + length - 1
                self.dp[i][j] = float('inf')
                for k in range(i, j):
                    q = self.dp[i][k] + self.dp[k + 1][j] + self.dimensions[i] * self.dimensions[k + 1] * self.dimensions[j + 1]
                    if q < self.dp[i][j]:
                        self.dp[i][j] = q
                        self.splits[i][j] = k

        #строение дерева
        def build_tree(i: int, j: int) -> Any: 
            
            if i == j:
                return self.matrices[i]['matrix_name']

            k = self.splits[i][j]
            left = build_tree(i, k)
            right = build_tree(k + 1, j)
            self.graph.add_edge(left, right, weight=1)
            return f"({left} x {right})"

        root = build_tree(0, self.n - 1)
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