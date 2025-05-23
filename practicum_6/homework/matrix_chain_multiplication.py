from pathlib import Path
from typing import Any, Union

import numpy as np
import networkx as nx

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class MatrixChainMultiplication:
    def __init__(self) -> None:
        self.graph = nx.Graph()

    def run(self, matrices: list[dict[str, Union[str, tuple[int, int]]]]) -> tuple[AnyNxGraph, str]:
        mats = matrices.copy()
        while len(mats) > 1:
            idx = max(range(len(mats) - 1), key=lambda i: mats[i]["shape"][1])
            left, right = mats[idx], mats[idx + 1]
            parent = left["matrix_name"] + right["matrix_name"]
            self.graph.add_edge(parent, left["matrix_name"])
            self.graph.add_edge(parent, right["matrix_name"])
            mats[idx:idx + 2] = [{"matrix_name": parent,
                                  "shape": (left["shape"][0], right["shape"][1])}]
        root = mats[0]["matrix_name"]
        return self.graph, root


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

