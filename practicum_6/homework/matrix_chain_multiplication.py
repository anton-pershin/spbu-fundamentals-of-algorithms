from pathlib import Path
from typing import Any, Union

import numpy as np
import networkx as nx

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class MatrixChainMultiplication:
    def __init__(self) -> None:
        self.graph = nx.Graph()
        self.node_cnt = 0

    def run(self, matrices: list[dict[str, Union[str, tuple[int, int]]]]) -> tuple[AnyNxGraph, Any]:
        n = len(matrices)

        if n == 0:
            return nx.Graph(), None
        dim = []
        for mat in matrices:
            rows, cols = mat["shape"]
            dim.append(rows)
        dim.append(matrices[-1]["shape"][1])

        m = [[0] * n for _ in range(n)]
        s = [[0] * n for _ in range(n)]

        for length in range(2, n + 1):  # длина цепочки от 2 до n
            for i in range(n - length + 1):
                j = i + length - 1
                m[i][j] = float('inf')
                for k in range(i, j):
                    cost = (m[i][k] + m[k + 1][j] + dim[i] * dim[k + 1] * dim[j + 1])

                    if cost < m[i][j]:
                        m[i][j] = cost
                        s[i][j] = k

        self.graph = nx.Graph()
        self.node_cnt = 0

        matrix_nodes = []
        for i in range(len(matrices)):
            mat = matrices[i]
            node_id = mat["matrix_name"]
            matrix_nodes.append(node_id)
            self.graph.add_node(node_id, label=mat["matrix_name"], type="leaf")

        if n == 1:
            root = matrix_nodes[0]
            return self.graph, root

        root = self._build_tree(matrix_nodes, s, 0, n - 1)

        return self.graph, root

    def _build_tree(self, matrix_nodes: list, s: list, i: int, j: int) -> Any:
        if i == j:
            return matrix_nodes[i]

        node_id = f"node_{self.node_cnt}"
        self.node_cnt += 1
        self.graph.add_node(node_id, label=f"M[{i},{j}]", type="internal")

        k = s[i][j]
        left_child = self._build_tree(matrix_nodes, s, i, k)
        right_child = self._build_tree(matrix_nodes, s, k + 1, j)

        self.graph.add_edge(node_id, left_child)
        self.graph.add_edge(node_id, right_child)

        return node_id

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