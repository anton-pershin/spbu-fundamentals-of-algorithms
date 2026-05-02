from pathlib import Path
from typing import Any, Union

import numpy as np
import networkx as nx

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class MatrixChainMultiplication:
    def __init__(self) -> None:

        self.graph = nx.Graph()
        self.split = None
        self.dimension = None

    def dimensions_limit(self, matrices):
        dimensions = [matrices[0]["shape"][0]]
        for m in matrices:
            dimensions.append(m["shape"][1])
        return dimensions

    def find_optimal_cost(self, dimensions):
        matrices_count = len(dimensions) - 1

        optimal_multiplication_cost = []
        split = []
        for _ in range(matrices_count):
            optimal_multiplication_cost.append([0] * matrices_count)
            split.append([0] * matrices_count)

        for chain_length in range(2, matrices_count + 1):
            for i in range(matrices_count - chain_length + 1):
                j = i + chain_length - 1
                optimal_multiplication_cost[i][j] = float("inf")

                for k in range(i, j):
                    cost = (
                        optimal_multiplication_cost[i][k]
                        + optimal_multiplication_cost[k + 1][j]
                        + dimensions[i] * dimensions[k + 1] * dimensions[j + 1]
                    )
                        
                    if cost < optimal_multiplication_cost[i][j]:
                        optimal_multiplication_cost[i][j] = cost
                        split[i][j] = k
                            
        return optimal_multiplication_cost, split

    def build_tree(self, matrices, i, j):
        if i == j:
            name = matrices[i]["matrix_name"]
            self.graph.add_node(name, label = name, type = "matrix")
            return name

        k = self.split[i][j]
        left = self.build_tree(matrices, i, k)
        right = self.build_tree(matrices, k + 1, j)
        node = f"multiplication_of_{i}_and_{j}"
    
        self.graph.add_node(node, label="*", type = "multiplication")
        self.graph.add_edge(node, left)
        self.graph.add_edge(node, right)

        return node
        
    def run(
        self,
        matrices: list[dict[str, Union[str, tuple[int, int]]]]
    ) -> tuple[AnyNxGraph, Any]:

        self.graph.clear()

        dimensions = self.dimensions_limit(matrices)
        self.dimension = dimensions

        _, self.split = self.find_optimal_cost(dimensions)

        root = self.build_tree(matrices, 0, len(matrices) - 1)

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

    print("root:", root)
    print("nodes:", matmul_tree.nodes)

    plot_graph(matmul_tree)

