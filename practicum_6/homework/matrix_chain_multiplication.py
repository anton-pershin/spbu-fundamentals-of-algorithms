from pathlib import Path
from typing import Any, Union

import numpy as np
import networkx as nx

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class MatrixChainMultiplication:
    def __init__(self) -> None:
        self.m = []
        self.shapes = []
        self.path = []
        self.tree = nx.Graph()
    
    def get_tree(self, i, j, names):
        if i == j:
            return names[i] 
        
        k = self.path[i][j]
        left = self.get_tree(i, k, names)
        right = self.get_tree(k + 1, j, names)
        return (left, right)

    @staticmethod
    def make_tree(t, G=None):
        if G is None:
            G = nx.Graph()

        G.add_node(t)
        if isinstance(t, tuple):
            left, right = t
            MatrixChainMultiplication.make_tree(left, G)
            MatrixChainMultiplication.make_tree(right, G)
            G.add_edge(t, left)
            G.add_edge(t, right)
            
        return G

    def run(
        self,
        matrices: list[dict[str, Union[str, tuple[int, int]]]]
    ) -> tuple[AnyNxGraph, Any]:

        shapes = [i["shape"][0] for i in matrices] + [matrices[-1]["shape"][1]]
        self.m = [[0] * len(matrices) for _ in range(len(matrices))]
        self.path = [[0] * len(matrices) for _ in range(len(matrices))]

        for size in range(2, len(matrices) + 1):
            for left in range(0, len(matrices) - size + 1):
                right = left + size - 1
                data = []

                for k in range(left, right):
                    data.append((self.m[left][k] + self.m[k+1][right] + shapes[left] * shapes[k+1] * shapes[right+1], k))

                data_min = min(data)
                self.m[left][right] = data_min[0]
                self.path[left][right] = data_min[1]

        names = [m['matrix_name'] for m in matrices]
        root_tuple = self.get_tree(0, len(matrices) - 1, names)
        self.tree = self.make_tree(root_tuple)

        mapping = {i:f"пустая вершина{j}" for j, i in enumerate(self.tree) if isinstance(i, tuple)}
        self.tree = nx.relabel_nodes(self.tree, mapping)

        return self.tree, root_tuple
        




                

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

