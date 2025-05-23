from pathlib import Path
from typing import Any, Union

import numpy as np
import networkx as nx
import itertools

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class MatrixChainMultiplication:
    def __init__(self) -> None:

        pass

    def run(
        self,
        matrices: list[dict[str, Union[str, tuple[int, int]]]]
    ) -> tuple[AnyNxGraph, Any]:
        if not matrices:
            return (nx.Graph(), None)

        sizes = [matrices[0]["shape"][0]] + [mat["shape"][1] for mat in matrices]
        n = len(matrices)
        m = [[0] * n for _ in range(n)]  # Минимальные затраты
        s = [[0] * n for _ in range(n)]  # Точки разделения

        for ch in range(2, n + 1):
            for i in range(n - ch + 1):
                j = i + ch - 1
                m[i][j], s[i][j] = min(
                    (m[i][k] + m[k+1][j] + sizes[i] * sizes[k+1] * sizes[j+1], k)
                    for k in range(i, j)
                )

        graph = nx.Graph()
        node_id = iter(f"M{i}" for i in itertools.count())  # Генератор имён

        def _add_node(i: int, j: int) -> str:
            if i == j:
                name = matrices[i]["matrix_name"]
                graph.add_node(name)
                return name
            else:
                k = s[i][j]
                left = _add_node(i, k)
                right = _add_node(k + 1, j)
                parent = next(node_id)
                graph.add_edges_from([(parent, left), (parent, right)])
                return parent

        root = _add_node(0, n-1)
        return (graph, root)



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

