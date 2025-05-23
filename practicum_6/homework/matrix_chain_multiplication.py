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

        n = len(matrices)  # количество матриц в цепочке

        p = [matrices[0]["shape"][0]] + [m["shape"][1] for m in matrices]  # цепочка размеров матриц
        m = np.full((n + 1, n + 1), np.inf)  # минимальное число операций умножения для матриц с i по j
        s = np.zeros((n + 1, n + 1), dtype=int)  # индексы разбиений между i и j

        for i in range(1, n + 1):
            m[i][i] = 0

        for length in range(2, n + 1):  # длина подцепочки
            for i in range(1, n - length + 2):
                j = i + length - 1
                for k in range(i, j):
                    cost = m[i][k] + m[k + 1][j] + p[i - 1] * p[k] * p[j]
                    if cost < m[i][j]:
                        m[i][j] = cost
                        s[i][j] = k

        graph = nx.Graph()

        def build_tree(i: int, j: int) -> str:
            if i == j:
                name = matrices[i - 1]["matrix_name"]
                graph.add_node(name, label="")
                return name
            else:
                k = s[i][j]
                left = build_tree(i, k)
                right = build_tree(k + 1, j)
                parent = f"({i},{j})"
                graph.add_node(parent, label="")
                graph.add_edges_from([(parent, left), (parent, right)])
                return parent

        root = build_tree(1, n)


        return graph, root


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
