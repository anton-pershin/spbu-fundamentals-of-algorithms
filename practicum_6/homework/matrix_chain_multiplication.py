from pathlib import Path
from typing import Any, Union

import numpy as np
import networkx as nx

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph

class Matrix():
    def __init__(
            self,
            shape: tuple[int, int] = (0, 0),
            complexity: int = 0,
            tree: list[tuple[str, str]] = []
    ) -> None:
        self.shape = shape
        self.complexity = complexity
        self.tree = tree 

    def __repr__(self) -> str:
        text = (
            f"\nShape: {self.shape}\n"
            f"Complexity: {self.complexity}\n"
            f"Tree: {self.tree}"
        )
        return text

class MatrixChainMultiplication:
    def __init__(self) -> None:
        self.matrices: dict[str, Matrix] = {}

    def preprocess(self, matrices) -> str:
        prod = str()
        for old in matrices:
            prod += old["matrix_name"]
            new = Matrix(old["shape"], 0, [])
            self.matrices[old["matrix_name"]] = new
        return prod

    def findChain(self, prod: str, tree: list[tuple[str, str]]) -> list[tuple[str, str]]:
        best = Matrix()
        for gap in range(1, len(prod)):
            leftProd = prod[:gap]
            rightProd = prod[gap:]

            if leftProd not in self.matrices:
                self.findChain(leftProd, [])
            if rightProd not in self.matrices:
                self.findChain(rightProd, [])

            # To this point, left and right will be in self.matrices
            left = self.matrices[leftProd]
            right = self.matrices[rightProd]

            shape = (left.shape[0], right.shape[1])
            complexity = left.complexity + right.complexity + \
                    shape[0] * shape[1] * left.shape[1]
            tree = [(prod, leftProd)] + [(prod, rightProd)] + left.tree + right.tree

            cur = Matrix(shape, complexity, tree)
            
            if best.complexity == 0 or cur.complexity < best.complexity:
                best = cur
        self.matrices[prod] = best

    def run(
        self,
        matrices: list[dict[str, Union[str, tuple[int, int]]]]
    ) -> tuple[AnyNxGraph, Any]:
        prod = self.preprocess(matrices)
        self.findChain(prod, [])
        
        matmul_tree = nx.DiGraph()
        matmul_tree.add_edges_from(self.matrices[prod].tree)
        root = matmul_tree.nodes[prod]
        return matmul_tree, root
        

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
    matmul_tree, root = mcm.run(test_matrices)

    plot_graph(matmul_tree)

