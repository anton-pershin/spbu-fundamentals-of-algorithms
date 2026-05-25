from pathlib import Path
from typing import Any, Union

import numpy as np
import networkx as nx

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class MatrixChainMultiplication:
    def __init__(self) -> None:
        self.count = 0
        self.sizes = []
        self.table_costs = []
        self.table_splits = []


    def run(
        self,
        matrices: list[dict[str, Union[str, tuple[int, int]]]]
    ) -> tuple[AnyNxGraph, Any]:
        self.count = len(matrices)
        self.sizes = []
        self.sizes.append(matrices[0]["shape"][0])
        for matrix in matrices:
            self.sizes.append(matrix["shape"][1])
        
        self.table_costs = np.zeros((self.count, self.count))
        self.table_splits = np.zeros((self.count, self.count)) 
        
        for length in range(2, self.count + 1):
            for start in range(self.count - length + 1):
                end = start + length - 1
                self.table_costs[start][end] = float('inf')

                for k in range(start, end):
                    cost = (self.table_costs[start][k] + self.table_costs[k + 1][end] + self.sizes[start] * self.sizes[k + 1] * self.sizes[end + 1])

                    if cost < self.table_costs[start][end]:
                        self.table_costs[start][end] = cost
                        self.table_splits[start][end] = k
        
        graph = nx.Graph()
        counter = [0]

        def build(start, end):
            if start == end:
                return matrices[start]["matrix_name"]
            
            k = int(self.table_splits[start][end])
            node_name = "node_" + str(counter[0])
            counter[0] += 1
            graph.add_node(node_name)

            left = build(start, k)
            right = build(k + 1, end)

            graph.add_edge(node_name, left)
            graph.add_edge(node_name, right)
            return node_name
        
        root = build(0, self.count - 1)
        return graph, root


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

