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
        if n == 0:
            raise ValueError("At least one matrix is required")

        p = [matrices[0]["shape"][0]] + [m["shape"][1] for m in matrices]

        m_cost = [[0 if i == j else float('inf') for j in range(n)] for i in range(n)]
        split = [[None for _ in range(n)] for _ in range(n)]

        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                for k in range(i, j):
                    cost = (m_cost[i][k] + m_cost[k+1][j] + p[i] * p[k+1] * p[j+1])
                    if cost < m_cost[i][j]:
                        m_cost[i][j] = cost
                        split[i][j] = k

        tree = nx.Graph()
        names = [m["matrix_name"] for m in matrices]
        node_counter = 0

        def build(i: int, j: int) -> Any:
            nonlocal node_counter
            if i == j:
                name = names[i]
                tree.add_node(name)
                return name
            k = split[i][j]
            left = build(i, k)
            right = build(k+1, j)
            node_id = f"N{node_counter}"
            node_counter += 1
            tree.add_node(node_id)
            tree.add_edge(node_id, left)
            tree.add_edge(node_id, right)
            return node_id

        root = build(0, n-1)
        return tree, root


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
