
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from pathlib import Path
from typing import Any, Union, List, Tuple

import numpy as np
import networkx as nx

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class MatrixChainMultiplication:
    def __init__(self) -> None:
        self.graph = nx.Graph()

    
    def _matrix_chain_order(
        self, 
        dims: List[int]
    ) -> Tuple[List[List[int]], 
         List[List[int]]]:
        n = len(dims) - 1
        m = [[0] * n for _ in range(n)]
        s = [[0] * n for _ in range(n)]

        for length in range(2, n + 1):  # the min number of matrices in a chain is 2 cuz chain of 1 matrix is kinda already multiplied
            for i in range(n - length + 1):
                j = i + length - 1
                m[i][j] = float('inf')
                for cut in range(i, j):
                    cost = m[i][cut] + m[cut + 1][j] + dims[i] * dims[cut + 1] * dims[j + 1]
                    if cost < m[i][j]:
                        m[i][j] = cost
                        s[i][j] = cut
                        
        return s, m
        

    def _build_tree(
        self, s: List[List[int]], 
        i: int, 
        j: int, 
        matrices: List[dict]
    ) -> str:
        if i == j:
            self.graph.add_node(matrices[i]['matrix_name'])
            return matrices[i]['matrix_name']
        else:
            cut = s[i][j]
            left = self._build_tree(s, i, cut, matrices)
            right = self._build_tree(s, cut + 1, j, matrices)
            node_id = f'({left} x {right})'
            self.graph.add_node(node_id)
            self.graph.add_edge(node_id, left)
            self.graph.add_edge(node_id, right)
            
            return node_id
        
    
    def run(
        self,
        matrices: list[dict[str, Union[str, tuple[int, int]]]]
    ) -> tuple[AnyNxGraph, Any]:
        dims = [matrix['shape'][0] for matrix in matrices] + [matrices[-1]['shape'][1]]
        s, m = self._matrix_chain_order(dims)
        root = self._build_tree(s, 0, len(matrices) - 1, matrices)    
        
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

    print(root)
    plot_graph(matmul_tree)





