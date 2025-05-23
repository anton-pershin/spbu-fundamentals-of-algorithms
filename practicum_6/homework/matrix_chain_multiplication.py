from pathlib import Path
from typing import Any, Union, Generator, Tuple
import networkx as nx
from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class MatrixChainMultiplication:
    def __init__(self) -> None:
        self._reset_state()

    def _reset_state(self) -> None:
        self._graph: nx.Graph = nx.Graph()
        self._root_node: Any = None
        self._matrices: list[dict] = []
        self._matrix_dims: list[int] = []
        self._matrix_names: list[str] = []
        self._dp_table: list[list[int]] = []
        self._split_points: list[list[int]] = []

    def run(
        self, 
        matrices: list[dict[str, Union[str, Tuple[int, int]]]]
    ) -> Tuple[AnyNxGraph, Any]:
        self._reset_state()
        self._matrices = matrices
        self._preprocess_input()
        self._compute_optimal_parenthesization()
        self._build_operation_tree()
        return self._graph, self._root_node

    def _preprocess_input(self) -> None:
        self._matrix_names = [m["matrix_name"] for m in self._matrices]
        self._matrix_dims = [self._matrices[0]["shape"][0]]
        self._matrix_dims.extend(m["shape"][1] for m in self._matrices)

    def _compute_optimal_parenthesization(self) -> None:
        n = len(self._matrices)
        self._dp_table = [[0]*n for _ in range(n)]
        self._split_points = [[0]*n for _ in range(n)]

        for chain_len in range(2, n+1):
            for i in range(n - chain_len + 1):
                j = i + chain_len - 1
                self._dp_table[i][j] = float('inf')
                
                for k in range(i, j):
                    cost = (self._dp_table[i][k] 
                            + self._dp_table[k+1][j] 
                            + self._matrix_dims[i] * self._matrix_dims[k+1] * self._matrix_dims[j+1])
                    
                    if cost < self._dp_table[i][j]:
                        self._dp_table[i][j] = cost
                        self._split_points[i][j] = k

    def _build_operation_tree(self) -> None:
        def recursive_builder(left: int, right: int) -> str:
            if left == right:
                matrix_name = self._matrix_names[left]
                self._graph.add_node(matrix_name, label=matrix_name, type='matrix')
                return matrix_name
            
            split = self._split_points[left][right]
            left_node = recursive_builder(left, split)
            right_node = recursive_builder(split+1, right)
            
            operation_id = f"Mul_{left}_{right}"
            self._graph.add_node(operation_id, 
                                label=f"Mul({left+1},{right+1})", 
                                type='operation')
            self._graph.add_edge(operation_id, left_node)
            self._graph.add_edge(operation_id, right_node)
            
            return operation_id

        self._root_node = recursive_builder(0, len(self._matrices)-1)


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

