from pathlib import Path
from typing import Any, Union

import numpy as np
import networkx as nx

import sys
sys.path.append('D:/spbu/spbu-fundamentals-of-algorithms/src')

from plotting.graphs import plot_graph
from common import AnyNxGraph

class MatrixChainMultiplication:
    def __init__(self) -> None:
        self.m = None
        self.s = None
        self.matrices = None
        self.node_counter = 0
        self.G = None

    def dp_tables(self) -> None:
        n = len(self.matrices)
        p = [self.matrices[0]['shape'][0]]
        for matrix in self.matrices:
            p.append(matrix['shape'][1])

        self.m = [[0] * n for _ in range(n)]
        self.s = [[0] * n for _ in range(n)]

        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                self.m[i][j] = float('inf')
                for k in range(i, j):
                    cost = (self.m[i][k] + self.m[k + 1][j] + p[i] * p[k + 1] * p[j + 1])
                    if cost < self.m[i][j]:
                        self.m[i][j] = cost
                        self.s[i][j] = k

    def build_tree(self, i: int, j: int) -> Any:
        if i == j:
            node_id = self.matrices[i]['matrix_name']
            self.G.add_node(node_id)
            return node_id
        else:
            node_id = f'node_{self.node_counter}'
            self.node_counter += 1
            k = self.s[i][j]
            left_child = self.build_tree(i, k)
            right_child = self.build_tree(k + 1, j)
            self.G.add_edge(node_id, left_child)
            self.G.add_edge(node_id, right_child)
            return node_id

    def run(self, matrices: list[dict[str, Union[str, tuple[int, int]]]]) -> tuple[AnyNxGraph, Any]:
        self.matrices = matrices
        self.node_counter = 0
        self.G = nx.Graph()

        self.dp_tables()

        n = len(matrices)
        root = self.build_tree(0, n - 1)

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
