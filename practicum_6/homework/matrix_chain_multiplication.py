from pathlib import Path
from typing import Any, Union

import numpy as np
import networkx as nx

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class MatrixChainMultiplication:
    def __init__(self) -> None:
        pass

    def run(
        self,
        matrices: list[dict[str, Union[str, tuple[int, int]]]]
    ) -> tuple[AnyNxGraph, Any]:
        
        n = len(matrices)

        p = [matrices[0]["shape"][0]]
        for m in matrices:
            p.append(m["shape"][1])
        
        m = np.zeros((n, n))
        s = np.zeros((n, n), dtype=int)

        for l in range(2, n + 1):
            for i in range(n - l + 1):
                j = i + l - 1
                m[i, j] = float('inf')
                for k in range(i, j):
                    cost = m[i, k] + m[k + 1, j] + p[i] * p[k + 1] * p[j + 1]
                    if cost < m[i, j]:
                        m[i, j] = cost
                        s[i, j] = k
        
        G = nx.DiGraph()
        counter = [0]
        
        def build_tree(i, j):
            if i == j:
                node_id = matrices[i]["matrix_name"]
                G.add_node(node_id)
                return node_id
            else:
                k = s[i, j]
                node_id = f"mult_{counter[0]}"
                counter[0] += 1
                G.add_node(node_id)
                left = build_tree(i, k)
                right = build_tree(k + 1, j)
                G.add_edge(node_id, left)
                G.add_edge(node_id, right)
                return node_id
        
        root = build_tree(0, n - 1)
        return G, root




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

