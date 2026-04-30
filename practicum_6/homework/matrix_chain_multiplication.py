from pathlib import Path
from typing import Any, Union

import numpy as np
import networkx as nx

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph

class Matrix():
    def __init__(
            self,
            prod: str,
            shape: tuple[int, int],
            complexity: int,
            tree: list[tuple[str, str]]
    ) -> None:
        self.prod = prod
        self.shape = shape
        self.complexity = complexity
        self.tree = tree 

    def __eq__(self, other) -> bool:
        if type(other) == str:
            return self.name == other
        return False

    def __repr__(self) -> str:
        text = (
            f"\nProduction: {self.prod}\n"
            f"Shape: {self.shape}\n"
            f"Complexity: {self.complexity}\n"
            f"Tree: {self.tree}"
        )
        return text

class MatrixChainMultiplication:
    def __init__(self) -> None:
        self.matrices: list[dict[str, str | tuple[int, int] | int]] = []
        self.bestTree: list[tuple[str, str]] = []

    def preprocess(self, matrices):
        for old in matrices:
            new = Matrix(old["matrix_name"], old["shape"], 0, [])
            self.matrices.append(new)

    def run(
        self,
        matrices: list[dict[str, Union[str, tuple[int, int]]]]
    ) -> tuple[AnyNxGraph, Any]:
        self.preprocess(matrices)
        print(self.matrices)


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
    mcm.run(test_matrices)
    #matmul_tree, root = mcm.run(test_matrices)

    #plot_graph(matmul_tree)

