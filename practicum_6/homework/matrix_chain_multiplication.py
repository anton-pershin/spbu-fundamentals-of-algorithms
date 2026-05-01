from pathlib import Path
from typing import Any, Union

import numpy as np
import networkx as nx

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class MatrixChainMultiplication:
    def __init__(self) -> None:
        self.G = nx.Graph()

    def run(
        self,
        matrices: list[dict[str, Union[str, tuple[int, int]]]]
    ) -> tuple[AnyNxGraph, Any]:
        
        n = len(matrices)
        m_sizes = [matrices[0]["shape"][0]] + [m["shape"][1] for m in matrices]
        min_paths = np.full((n, n), np.inf)
        dividers = np.zeros((n, n), dtype = int)

        for i in range(0, n):
            min_paths[i, i] = 0
        
        for l in range(1, n):
            for i in range(0, n - l):
                j = i + l
                for k in range(i, j):
                    if (min_paths[i, j]) > (min_paths[i, k] + min_paths[k + 1, j] + m_sizes[i] * m_sizes[k+1] * m_sizes[j+1]):
                        min_paths[i, j] = min_paths[i, k] + min_paths[k + 1, j] + m_sizes[i] * m_sizes[k+1] * m_sizes[j+1]
                        dividers[i, j] = k
        
        root = self.make_tree(dividers, 0, n - 1, matrices)
        return self.G, root


    def make_tree(self, dividers, begin_m: int, end_m: int, matrices: list[dict[str, Union[str, tuple[int, int]]]]):
        if begin_m == end_m:
            name = matrices[begin_m]["matrix_name"]
            self.G.add_node(name)
            return name
        
        k = int(dividers[begin_m, end_m])
        left_child = self.make_tree(dividers, begin_m, k, matrices)
        right_child = self.make_tree(dividers, k + 1, end_m, matrices)
        
        current_node = f"{matrices[begin_m]["matrix_name"]}->{matrices[end_m]["matrix_name"]}"
        self.G.add_edge(current_node, left_child)
        self.G.add_edge(current_node, right_child)
        
        return current_node
        

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

