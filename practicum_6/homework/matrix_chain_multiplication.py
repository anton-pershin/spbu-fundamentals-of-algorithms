from pathlib import Path
from typing import Any, Union

import numpy as np
import networkx as nx

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class MatrixChainMultiplication:
    def __init__(self) -> None:
        self.graph = nx.Graph()
        self.node_counter = 0
        self.split = None

    def build_tree(self, i: int, j: int, ids: list[str]) -> str:
        if i == j:
            self.graph.add_node(ids[i])
            return ids[i]
        
        k = self.split[i, j]
        left_child = self.build_tree(i, k, ids)
        right_child = self.build_tree(k + 1, j, ids)

        parent_node = f"m_{self.node_counter}"
        self.node_counter += 1

        self.graph.add_edge(parent_node, left_child)
        self.graph.add_edge(parent_node, right_child) 

        return parent_node       

    def run(
        self,
        matrices: list[dict[str, Union[str, tuple[int, int]]]]
    ) -> tuple[AnyNxGraph, Any]:
        self.graph = nx.Graph()
        self.node_counter = 0

        ids = [n["matrix_name"] for n in matrices]
        shapes = [m["shape"] for m in matrices]

        n = len(matrices)

        if n == 1:
            self.graph.add_node(ids[0])
            return self.graph, ids[0]
        
        p = [shapes[0][0]]
        for r, c in shapes:
            p.append(c)

        cost = np.full((n, n), 10**18, dtype=np.int64)
        np.fill_diagonal(cost, 0)
        self.split = np.full((n, n), -1, dtype=np.int64)

        for leng in range(2, n + 1):
            for i in range(0, n - leng + 1):
                j = i + leng - 1
                for k in range(i, j):
                    cur_cost = (cost[i, k] + cost[k + 1, j] + p[i] * p[k + 1] * p[j + 1])
                    if cur_cost < cost[i, j]:
                        cost[i, j] = cur_cost
                        self.split[i, j] = k

        root = self.build_tree(0, n - 1, ids)
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

    plot_graph(matmul_tree)

