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
        # Список матриц в два массива (названия и размеры)
        matrix_shapes = [(m["shape"][0], m["shape"][1]) for m in matrices]
        matrix_names = [m["matrix_name"] for m in matrices]
    
        # Проверка возможности перемножения
        for idx in range(len(matrix_shapes)-1):
            if matrix_shapes[idx][1] != matrix_shapes[idx+1][0]:
                raise ValueError(f"Матрицы {idx}-й и {(idx+1)}-й нельзя перемножить.")
    
        # Таблицы для хранения минимальной стоимости и оптимальных разделений
        m = np.zeros((n, n), dtype=np.int64)
        s = np.zeros((n, n), dtype=np.int64)
    
        # Минимальные затраты на перемножение
        for chain_len in range(2, n + 1):
            for i in range(n - chain_len + 1):
                j = i + chain_len - 1
                m[i,j] = float('inf')  # начальное кол-во операций бесконечно большое
            
                for k in range(i, j):
                    #Расчёт стоимости операции
                    cost = m[i,k] + m[k+1,j] + (matrix_shapes[i][0] * matrix_shapes[k][1] * matrix_shapes[j][1])
                    if cost < m[i,j]:
                        m[i,j] = cost
                        s[i,j] = k
                        
        # Построение дерева
        graph = nx.DiGraph()
        next_node_id = 0
    
        def build_graph(i: int, j: int, parent_id: Optional[str]) -> None:
            nonlocal next_node_id
            if i == j:
                matrix = matrix_names[i]
                graph.add_node(matrix, label=matrix)
                if parent_id is not None:
                    graph.add_edge(parent_id, matrix)
            else:
                current_id = f'node_{next_node_id}'
                next_node_id += 1
                graph.add_node(current_id, label=f'(M{i+1}:M{j+1})')
                if parent_id is not None:
                    graph.add_edge(parent_id, current_id)
                k = s[i,j]
                build_graph(i, k, current_id)
                build_graph(k+1, j, current_id)
        
        # Построение дерева 
        root_id = f'node_{next_node_id}'
        next_node_id +=1 
        graph.add_node(root_id, label='ROOT')
        build_graph(0, n-1, root_id)
    
        return graph, root_id



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

