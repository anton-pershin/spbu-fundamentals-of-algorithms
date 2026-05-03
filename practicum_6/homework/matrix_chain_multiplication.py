from pathlib import Path
from typing import Any, Union

import numpy as np
import networkx as nx

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class MatrixChainMultiplication:
    def __init__(self) -> None:
        self.G = nx.Graph()
        self.cost = np.array([])
        self.split = np.array([])
        self.dims = []
        self.count = 0

    def build_tree(self, i: int, j: int, matrices: list[dict[str, Union[str, tuple[int, int]]]]) -> str:
        if i == j:
            return matrices[i]["matrix_name"]

        k = int(self.split[i, j])
        left_child = self.build_tree(i, k, matrices)
        right_child = self.build_tree(k + 1, j, matrices)

        node_id = f"internal_{self.count}"
        self.count += 1
        
        self.G.add_node(node_id)
        self.G.add_edge(node_id, left_child)
        self.G.add_edge(node_id, right_child)
        return node_id

    def run(
        self,
        matrices: list[dict[str, Union[str, tuple[int, int]]]]
    ) -> tuple[AnyNxGraph, Any]:
        n = len(matrices)
        if n == 0:
            return nx.Graph(), None
        if n == 1:
            g = nx.Graph()
            g.add_node(matrices[0]["matrix_name"])
            return g, matrices[0]["matrix_name"]

        self.dims = [matrices[0]["shape"][0]] + [m["shape"][1] for m in matrices]

        self.cost = np.full((n, n), np.inf)
        self.split = np.zeros((n, n), dtype=int)

        for i in range(n):
            self.cost[i, i] = 0

        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                for k in range(i, j):
                    cost = (self.cost[i, k] + 
                            self.cost[k + 1, j] + 
                            self.dims[i] * self.dims[k + 1] * self.dims[j + 1])
                    
                    if cost < self.cost[i, j]:
                        self.cost[i, j] = cost
                        self.split[i, j] = k

        self.G = nx.Graph()
        self.count = 0
        root = self.build_tree(0, n - 1, matrices)

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

