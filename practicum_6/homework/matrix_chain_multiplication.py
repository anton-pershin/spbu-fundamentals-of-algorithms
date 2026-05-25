from pathlib import Path
from typing import Any, Union

import numpy as np
import networkx as nx

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class MatrixChainMultiplication:
    def __init__(self) -> None:
        self.node_counter = 0

    def run(
        self,
        matrices: list[dict[str, Union[str, tuple[int, int]]]]
    ) -> tuple[AnyNxGraph, Any]:
        
        n = len(matrices)
        
        if n == 0:
            return nx.Graph(), None
        if n == 1:
            g = nx.Graph()
            node_id = matrices[0]["matrix_name"]
            g.add_node(node_id)
            return g, node_id

        p = [matrices[0]["shape"][0]] + [m["shape"][1] for m in matrices]

        m = np.zeros((n, n))
        s = np.zeros((n, n), dtype=int)

        for L in range(2, n + 1):
            for i in range(n - L + 1):
                j = i + L - 1
                m[i, j] = float('inf')
                for k in range(i, j):
                    q = m[i, k] + m[k + 1, j] + p[i] * p[k + 1] * p[j + 1]
                    if q < m[i, j]:
                        m[i, j] = q
                        s[i, j] = k

        G = nx.Graph()
        self.node_counter = 0

        def build_tree(i: int, j: int) -> str:
            if i == j:
                node_id = matrices[i]["matrix_name"]
                G.add_node(node_id)
                return node_id

            k = s[i, j]

            left_child = build_tree(i, k)
            right_child = build_tree(k + 1, j)

            self.node_counter += 1
            node_id = f"Op_{self.node_counter}"

            G.add_node(node_id)
            G.add_edge(node_id, left_child)
            G.add_edge(node_id, right_child)

            return node_id

        root_id = build_tree(0, n - 1)

        return G, root_id


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