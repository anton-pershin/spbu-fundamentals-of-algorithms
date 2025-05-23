from pathlib import Path
from typing import Any, Union

import numpy as np
import networkx as nx

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class MatrixChainMultiplication:
    def __init__(self) -> None:
        self.min_ops = None
        self.opt_splits = None
        self.mingraph = nx.Graph()
        self.node_name = 1
        self.root = None

    def run(
        self,
        matrices: list[dict[str, Union[str, tuple[int, int]]]]
    ) -> tuple[AnyNxGraph, Any]:

        lenlist = []
        for matrix in matrices:
            lenlist.append(matrix["shape"][0])
        lenlist.append(matrices[-1]["shape"][1])

        n = len(lenlist) - 1
        self.min_ops = np.zeros((n, n))
        self.opt_splits = np.zeros((n, n), dtype=np.int64)

        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                self.min_ops[i][j] = np.float64('inf')
                
                for k in range(i, j):
                    cost = (self.min_ops[i][k] + self.min_ops[k+1][j] + lenlist[i] * lenlist[k+1] * lenlist[j+1])
                    if cost < self.min_ops[i][j]:
                        self.min_ops[i][j] = cost
                        self.opt_splits[i][j] = k

        nodes = {}
        for i in range(n):
            Node = matrices[i]["matrix_name"]
            self.mingraph.add_node(Node, type="leaf")
            nodes[(i, i)] = Node
        
        stack = []
        stack.append((0, n - 1, False))

        while stack:
            i, j, visited = stack.pop()
            if i == j:
                continue
            k = self.opt_splits[i][j]
            if not visited:
                stack.append((i, j, True))
                stack.append((k+1, j, False))
                stack.append((i, k, False))
            else:
                left = nodes[(i, k)]
                right = nodes[(k+1, j)]
                
                new_name = f"N{self.node_name}"
                self.node_name += 1
                
                self.mingraph.add_node(new_name, type="stem")
                self.mingraph.add_edge(new_name, left)
                self.mingraph.add_edge(new_name, right)
                
                nodes[(i, j)] = new_name
                self.root = new_name

        return self.mingraph, self.root


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

