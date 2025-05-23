from pathlib import Path
from typing import Any, Union

import numpy as np
import networkx as nx

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class MatrixChainMultiplication:
    def __init__(self) -> None:
        self.G = None
        self.root = None
        self.matrices = None
        self.n = 0
        self.p = []
        self.matrix_names = []
        self.m = []
        self.s = []

    def run(
        self,
        matrices: list[dict[str, Union[str, tuple[int, int]]]]
    ) -> tuple[AnyNxGraph, Any]:
        self.matrices = matrices
        self.n = len(matrices)
        self.p = [matrices[0]["shape"][0]]
        for m in matrices:
            self.p.append(m["shape"][1])
        self.matrix_names = [m["matrix_name"] for m in matrices]
        self.m = [[0] * self.n for _ in range(self.n)]
        self.s = [[0] * self.n for _ in range(self.n)]

        # Динамическое программирование
        for l in range(2, self.n + 1):
            for i in range(self.n - l + 1):
                j = i + l - 1
                self.m[i][j] = float('inf')
                for k in range(i, j):
                    q = (
                        self.m[i][k]
                        + self.m[k + 1][j]
                        + self.p[i] * self.p[k + 1] * self.p[j + 1]
                    )
                    if q < self.m[i][j]:
                        self.m[i][j] = q
                        self.s[i][j] = k

        # Восстановление дерева
        self.G = nx.Graph()

        def build_tree(i, j, node_id_gen):
            if i == j:
                name = self.matrix_names[i]
                self.G.add_node(name, label=name)
                return name
            else:
                k = self.s[i][j]
                left = build_tree(i, k, node_id_gen)
                right = build_tree(k + 1, j, node_id_gen)
                node_id = next(node_id_gen)
                self.G.add_node(node_id, label="")
                self.G.add_edge(node_id, left)
                self.G.add_edge(node_id, right)
                return node_id

        def node_id_generator():
            idx = 0
            while True:
                yield f"mul_{idx}"
                idx += 1

        self.root = build_tree(0, self.n - 1, node_id_generator())
        return self.G, self.root

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