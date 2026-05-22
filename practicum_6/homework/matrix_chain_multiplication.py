from pathlib import Path
from typing import Any, Union

import numpy as np
import networkx as nx

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class MatrixChainMultiplication:
    def __init__(self) -> None:

        self.G = nx.Graph()


    def make_tree(self, matrices: list[dict[str, Union[str, tuple[int, int]]]], dividors: np.ndarray, begin_m: int, end_m: int) -> str:
        if begin_m == end_m:
            return matrices[begin_m]["matrix_name"]
    
        k = int(dividors[begin_m, end_m])

        left_child = self.make_tree(matrices, dividors, begin_m, k)
        right_child = self.make_tree(matrices, dividors, k + 1, end_m)
        
        current_node = f"({matrices[begin_m]["matrix_name"]}->{matrices[end_m]["matrix_name"]})"
        
        self.G.add_node(current_node)
        self.G.add_edge(current_node, left_child)
        self.G.add_edge(current_node, right_child)
        
        return current_node


    
    def run(
        self,
        matrices: list[dict[str, Union[str, tuple[int, int]]]]
    ) -> tuple[AnyNxGraph, Any]:

        length = len(matrices)
        sizes = [matrices[0]["shape"][0]] + [matr["shape"][1] for matr in matrices]
        min_paths = np.full((length, length), np.inf)
        dividors = np.zeros((length, length))
        
        for i in range(length):
            min_paths[i, i] = 0

        for l in range (1, length):
            for i in range(length-l):
                j = i+l
                for k in range(i, j):
                    if (min_paths[i, j]) > (min_paths[i, k] + min_paths[k+1, j] + sizes[i]*sizes[k+1]+sizes[j+1]):
                        min_paths[i, j] = min_paths[i, k] + min_paths[k+1, j] + sizes[i]*sizes[k+1]+sizes[j+1]
                        dividors[i, j] = k
        

        root = self.make_tree(matrices, dividors, 0, length-1)

        return[self.G, root]


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

