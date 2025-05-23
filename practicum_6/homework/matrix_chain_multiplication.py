from pathlib import Path
from typing import Any, Union, Tuple, List

import numpy as np
import networkx as nx

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class MatrixChainMultiplication:
    def __init__(self) -> None:
        self.G = None

    def run(
        self,
        matrices: List[dict[str, Union[str, Tuple[int, int]]]]
    ) -> Tuple[AnyNxGraph, Any]:
        n = len(matrices)
        if n == 0:
            return nx.Graph(), None
        
        p = [matrices[i]['shape'][0] for i in range(n)] + [matrices[-1]['shape'][1]]
        cost = [[0]*n for _ in range(n)]
        split = [[0]*n for _ in range(n)]

        for l in range(1, n):
            for i in range(n - l):
                j = i + l
                best = min(
                    (cost[i][k] + cost[k+1][j] + p[i]*p[k+1]*p[j+1], k)
                    for k in range(i, j)
                )
                cost[i][j], split[i][j] = best

        G = nx.Graph()
        def build(i: int, j: int) -> Any:
            if i == j:
                name = matrices[i]['matrix_name']
                G.add_node(name)
                return name
            k = split[i][j]
            left = build(i, k)
            right = build(k+1, j)
            node = (i, j)
            G.add_node(node)
            G.add_edge(node, left)
            G.add_edge(node, right)
            return node

        root = build(0, n-1)
        self.G = G
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

