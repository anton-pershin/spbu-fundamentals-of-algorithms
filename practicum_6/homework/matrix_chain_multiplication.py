from pathlib import Path
from typing import Any, Union

import numpy as np
import networkx as nx

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class MatrixChainMultiplication:
    def __init__(self) -> None:
        self.G = nx.DiGraph()

    def run(
        self,
        matrices: list[dict[str, Union[str, tuple[int, int]]]]
    ) -> tuple[AnyNxGraph, Any]:
        
        matrix_names = [m["matrix_name"] for m in matrices]
        shapes = [m["shape"] for m in matrices]
        dims = [shapes[0][0]] + [shape[1] for shape in shapes]
        n = len(dims) - 1

        min_operations = [[0] * n for _ in range(n)]
        split = [[-1] * n for _ in range(n)]

        for lengh in range(2, n + 1): # шаг
            for i in range(n - lengh + 1): # начало
                j = i + lengh - 1
                min_operations[i][j] = float('inf')
                for k in range(i, j): # идем от i до j 
                    cost = min_operations[i][k] + min_operations[k + 1][j] + dims[i] * dims[k + 1] * dims[j + 1]
                    if cost < min_operations[i][j]:
                        min_operations[i][j] = cost # находим минимальное количество операци на каждом шаге
                        split[i][j] = k

        self.G = nx.DiGraph()
        count = 0

        def build_tree(i, j):
            nonlocal count
            if i == j:
                return matrix_names[i]
            k = split[i][j]
            left = build_tree(i, k)
            right = build_tree(k + 1, j)
            node_id = (f"node_{count}")
            count += 1
            self.G.add_node(node_id)
            self.G.add_edge(node_id, left)
            self.G.add_edge(node_id, right)
            return node_id

        root = build_tree(0, n - 1)
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