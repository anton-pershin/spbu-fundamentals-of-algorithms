from pathlib import Path
from typing import Any, Union

import numpy as np
import networkx as nx

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class MatrixChainMultiplication:
    def __init__(self) -> None:
        self.node_id = 0
        self.dp = None
        self.dims = None
        self.split = None

    def run(
        self,
        matrices: list[dict[str, Union[str, tuple[int, int]]]]
    ) -> tuple[AnyNxGraph, Any]:

        num = len(matrices)

        dimensions = [matrices[0]["shape"][0]]
        for matrix in matrices:
            dimensions.append(matrix["shape"][1])

        self.dims = dimensions

        min_cost = [[0] * num for _ in range(num)]
        split = [[0] * num for _ in range(num)]

        for length in range(2, num + 1):
            for start in range(num - length + 1):
                end = start + length - 1
                min_cost[start][end] = float("inf")

                for split_point in range(start, end):
                    cost = (
                        min_cost[start][split_point] + min_cost[split_point + 1][end]
                        + dimensions[start] * dimensions[split_point + 1] * dimensions[end + 1]
                    )

                    if cost < min_cost[start][end]:
                        min_cost[start][end] = cost
                        split[start][end] = split_point

        self.dp = min_cost
        self.split = split

        G = nx.Graph()

        def build_tree(start, end):
            if start == end:
                name = matrices[start]["matrix_name"]
                G.add_node(name, label=name)
                return name

            split_point = split[start][end]

            left = build_tree(start, split_point)
            right = build_tree(split_point + 1, end)

            self.node_id += 1
            operation_node = f"mul_{self.node_id}"
            
            G.add_node(operation_node, label="*")
            G.add_edge(operation_node, left)
            G.add_edge(operation_node, right)

            return operation_node

        root = build_tree(0, num - 1)

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