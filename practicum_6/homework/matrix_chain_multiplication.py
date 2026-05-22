from pathlib import Path
from typing import Any, Union

import numpy as np
import networkx as nx

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class MatrixChainMultiplication:
    def __init__(self) -> None:
        self._graph: AnyNxGraph | None = None
        self._root: Any | None = None

    def run(
        self,
        matrices: list[dict[str, Union[str, tuple[int, int]]]]
    ) -> tuple[AnyNxGraph, Any]:
        if not matrices:
            raise ValueError("matrix list must not be empty")

        matrix_names = []
        shapes = []
        for matrix in matrices:
            name = matrix.get("matrix_name")
            shape = matrix.get("shape")
            if not isinstance(name, str):
                raise TypeError("matrices must have name")
            if (
                not isinstance(shape, tuple)
                or len(shape) != 2
                or not all(isinstance(v, int) for v in shape)
            ):
                raise TypeError("matrices must have shape")
            matrix_names.append(name)
            shapes.append(shape)

        n = len(shapes)
        dims = [shapes[0][0]] + [shape[1] for shape in shapes]

        for i in range(1, n):
            if shapes[i - 1][1] != shapes[i][0]:
                raise ValueError(
                    f"matrices shapes are incompatible:  "
                    f"{shapes[i - 1]} and {shapes[i]}"
                )

        cost = [[0] * n for _ in range(n)]
        split = [[None] * n for _ in range(n)]

        for length in range(2, n + 1):
            for i in range(0, n - length + 1):
                j = i + length - 1
                best_cost = float("inf")
                best_k = None
                for k in range(i, j):
                    current_cost = (
                        cost[i][k]
                        + cost[k + 1][j]
                        + dims[i] * dims[k + 1] * dims[j + 1]
                    )
                    if current_cost < best_cost:
                        best_cost = current_cost
                        best_k = k
                cost[i][j] = best_cost
                split[i][j] = best_k

        graph = nx.Graph()

        def build_tree(i: int, j: int) -> Any:
            if i == j:
                node_id = matrix_names[i]
                graph.add_node(node_id)
                return node_id
            k = split[i][j]
            left = build_tree(i, k)
            right = build_tree(k + 1, j)
            node_id = (i, j)
            graph.add_node(node_id)
            graph.add_edge(node_id, left)
            graph.add_edge(node_id, right)
            return node_id

        root = build_tree(0, n - 1)
        self._graph = graph
        self._root = root

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
