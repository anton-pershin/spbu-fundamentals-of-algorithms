import sys
from pathlib import Path

root_path = Path(__file__).resolve().parents[2]
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))

from typing import Any, Union
import numpy as np
import networkx as nx

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class MatrixChainMultiplication:
    def __init__(self) -> None:
        self.node_counter = 0

    def build_tree(self, i: int, j: int, s_table: list, matrices: list, graph: nx.Graph) -> Any:
        if i == j:
            node_name = matrices[i]["matrix_name"]
            graph.add_node(node_name)
            return node_name

        k = s_table[i][j]
        
        left_child = self.build_tree(i, k, s_table, matrices, graph)
        right_child = self.build_tree(k + 1, j, s_table, matrices, graph)

        parent_node = f"node_{self.node_counter}"
        self.node_counter += 1

        graph.add_node(parent_node)
        graph.add_edge(parent_node, left_child)
        graph.add_edge(parent_node, right_child)

        return parent_node

    def run(
        self,
        matrices: list[dict[str, Union[str, tuple[int, int]]]]
    ) -> tuple[AnyNxGraph, Any]:
        
        n = len(matrices)
        if n == 0:
            return nx.Graph(), None

        p = []
        p.append(matrices[0]["shape"][0])
        for m in matrices:
            p.append(m["shape"][1])

        m_table = [[0] * n for _ in range(n)]
        s_table = [[0] * n for _ in range(n)]

        for length in range(2, n + 1):
            for i in range(0, n - length + 1):
                j = i + length - 1
                m_table[i][j] = float("inf")
                
                for k in range(i, j):
                    q = m_table[i][k] + m_table[k + 1][j] + p[i] * p[k + 1] * p[j + 1]
                    if q < m_table[i][j]:
                        m_table[i][j] = q
                        s_table[i][j] = k

        graph = nx.Graph()
        self.node_counter = 0
        root = self.build_tree(0, n - 1, s_table, matrices, graph)

        return graph, root


if __name__ == "__main__":
    test_matrices = [
        {"matrix_name": "A", "shape": (2, 3)},
        {"matrix_name": "B", "shape": (3, 10)},
        {"matrix_name": "C", "shape": (10, 20)},
        {"matrix_name": "D", "shape": (20, 3)},
    ]

    mcm = MatrixChainMultiplication()
    matmul_tree, root = mcm.run(test_matrices)

    plot_graph(matmul_tree)