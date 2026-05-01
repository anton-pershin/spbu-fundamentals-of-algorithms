from pathlib import Path
from typing import Any, Union

import numpy as np
import networkx as nx

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class MatrixChainMultiplication:
    def __init__(self) -> None:
        self.graph = nx.Graph()
        self.id = 0

    def run(
        self,
        matrices: list[dict[str, Union[str, tuple[int, int]]]]
    ) -> tuple[AnyNxGraph, Any]:
        n = len(matrices)
        m = {(i,j): float('inf') for i in range(1, n+1) for j in range(i, n+1)}
        s={}
        d = [matrices[0]["shape"][0]] + [x["shape"][1] for x in matrices]
    
        for i in range(1, n+1):
            m[(i,i)] = 0
        
        for i in range(1, n+1):
            for j in range(i, n+1):
                if i == j:
                    m[(i,j)] = 0
                else:
                    best = None
                    best_c = float('inf')
                    for k in range(i, j):
                        c = m[(i,k)] + m[(k+1,j)] + d[i-1] * d[k] * d[j] 
                        if c< best_c:
                            best = k
                            best_c = c

                    m[(i,j)] = best_c
                    s[(i,j)] = best
        G = self.graph
        self.id = 0
        def build(i,j):
            if i == j:
                name = matrices[i-1]["matrix_name"]
                G.add_node(name)
                return name
            k = s[(i,j)]
            self.id+=1
            root = f"{self.id}"
            G.add_node(root)
            left = build(i,k)
            right = build(k+1,j)
            G.add_edge(root,left)
            G.add_edge(root,right)
            return root
        root = build(1,n)
        return G,root


        


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
    print(root)

