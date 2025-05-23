from pathlib import Path
from typing import Any, Union

import numpy as np
import networkx as nx

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class MatrixChainMultiplication:
    def __init__(self) -> None:
        self.graph = None
        self.res_root = ""

    def run(
        self,
        matrices: list[dict[str, Union[str, tuple[int, int]]]]
    ) -> tuple[AnyNxGraph, Any]:
        self.graph = nx.Graph()
        for i in range(len(matrices) - 1):
            max_line = 0
            max_matrix = ""
            new_node = ""
            new_m = 0
            new_n = 0
            l_node = ""
            r_node = ""
            for el in range(len(matrices) - 1):
                if matrices[el]["shape"][1] > max_line:
                    max_line = matrices[el]["shape"][1]
                    max_matrix = matrices[el]["matrix_name"]
                    new_node = matrices[el]["matrix_name"] + matrices[el + 1]["matrix_name"]
                    new_m = matrices[el]["shape"][0]
                    new_n = matrices[el + 1]["shape"][1]
                    l_node = matrices[el]["matrix_name"]
                    r_node = matrices[el + 1]["matrix_name"]

            for el in range(len(matrices) - 1):
                if matrices[el]["matrix_name"] == l_node:
                    matrices.insert(el + 1, {"matrix_name": new_node, "shape": (new_m, new_n)})
            self.res_root = matrices[0]["matrix_name"]
            matrices = [el for el in matrices if (el["shape"][1] != max_line and el["shape"][0] != max_line)]

            self.graph.add_edge(new_node, l_node)
            self.graph.add_edge(new_node, r_node)

        res = (self.graph, self.res_root)
        return res

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

