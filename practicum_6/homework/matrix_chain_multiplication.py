from pathlib import Path
from typing import Any, Union

import numpy as np
import networkx as nx
import sys
sys.path.append(r"/home/viktoria/algoritms/spbu-fundamentals-of-algorithms")
from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class MatrixChainMultiplication:
    def __init__(self) -> None:
        self.G = None
        self.root = None
        self.X = None
        self.N = 0
        self.D = []
        self.L = []
        self.T = []
        self.K = []

    def run(
        self,
        matrices: list[dict[str, Union[str, tuple[int, int]]]]
    ) -> tuple[AnyNxGraph, Any]:
        self.X = matrices
        self.N = len(matrices)
        self.D = [matrices[0]["shape"][0]] + [x["shape"][1] for x in matrices]
        self.L = [x["matrix_name"] for x in matrices]
        self.T = [[0]*self.N for _ in range(self.N)]
        self.K = [[0]*self.N for _ in range(self.N)]

        for d in range(2, self.N+1):
            for i in range(self.N-d+1):
                j = i+d-1
                self.T[i][j] = float('inf')
                for r in range(i, j):
                    v = self.T[i][r] + self.T[r+1][j] + self.D[i]*self.D[r+1]*self.D[j+1]
                    if v < self.T[i][j]:
                        self.T[i][j] = v
                        self.K[i][j] = r

        self.G = nx.Graph()

        def U(i, j, g):
            if i == j:
                n = self.L[i]
                self.G.add_node(n, label=n)
                return n
            else:
                r = self.K[i][j]
                a = U(i, r, g)
                b = U(r+1, j, g)
                c = next(g)
                self.G.add_node(c, label="")
                self.G.add_edge(c, a)
                self.G.add_edge(c, b)
                return c

        def G():
            i = 0
            while True:
                yield f"_{i}_"
                i += 1

        self.root = U(0, self.N-1, G())
        return self.G, self.root


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