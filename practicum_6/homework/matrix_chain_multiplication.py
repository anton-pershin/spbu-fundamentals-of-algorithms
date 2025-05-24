from pathlib import Path
from typing import *

import numpy as np
import networkx as nx

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class MatrixChainMultiplication:
    
    def __init__(self) -> None:
        self.graph = nx.Graph()
        self.root = None
        self.shapes = {}
        self.node_id = 0

    def run(
        self,
        matrices: List[Dict[str, Union[str, Tuple[int, int]]]]
    ) -> Tuple[AnyNxGraph, str]:
        n = len(matrices)
        self.shapes = {m["matrix_name"]: m["shape"] for m in matrices}
        names = [m["matrix_name"] for m in matrices]

        m = [[0] * n for _ in range(n)]
        s = [[-1] * n for _ in range(n)]

        for chain_len in range(2, n + 1):
            for i in range(n - chain_len + 1):
                j = i + chain_len - 1
                m[i][j] = float('inf')
                for k in range(i, j):
                    cost = (
                        m[i][k] + m[k + 1][j] +
                        self.shapes[names[i]][0] *
                        self.shapes[names[k]][1] *
                        self.shapes[names[j]][1]
                    )
                    if cost < m[i][j]:
                        m[i][j] = cost
                        s[i][j] = k

        self.graph.clear()
        self.node_id = 0
        self.root = self._build_tree(s, names, 0, n - 1)
        return self.graph, self.root

    def _build_tree(self, s, names, i, j):
        if i == j:
            return names[i]
        k = s[i][j]
        left = self._build_tree(s, names, i, k)
        right = self._build_tree(s, names, k + 1, j)
        node_name = f"Node_{self.node_id}"
        self.node_id += 1
        self.graph.add_node(node_name)
        self.graph.add_edge(node_name, left)
        self.graph.add_edge(node_name, right)
        return node_name


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

