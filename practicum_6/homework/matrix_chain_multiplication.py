import sys
from pathlib import Path
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

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

        """
        Нахождение оптимального порядка умножения цепочки матриц и
        построение дерева этих умножений в виде графа.

        matrices: список словарей с ключами:
        - 'matrix_name': имя матрицы (строка)
        - 'shape': кортеж (число строк, число столбцов)

        Результат:
        graph: nx.Graph, в котором листья — исходные матрицы,
        а внутренние узлы — операции умножения;
        root: идентификатор корневого узла (точка последнего умножения).
        """
        n = len(matrices)
        # Строим список размеров p: p[0]=число строк первой,
        # p[1]=число столбцов первой (и строк второй), ..., p[n]=число столбцов последней
        p = [matrices[0]['shape'][0]]
        for m in matrices:
            p.append(m['shape'][1])

        # m_cost[i][j] — минимальное количество скалярных умножений для цепочки с i по j
        # s_split[i][j] — индекс k, при котором достигается минимум для (i,j)
        m_cost = [[0] * n for _ in range(n)]
        s_split = [[0] * n for _ in range(n)]

        # Длина цепочки от 2 до n
        for length in range(2, n + 1):
            # i — начало цепочки (0..n-length)
            for i in range(n - length + 1):
                j = i + length - 1  # конец цепочки
                m_cost[i][j] = float('inf')
                # Пробуем все разбиения i..k и k+1..j
                for k in range(i, j):
                    cost = (
                        m_cost[i][k] + m_cost[k + 1][j]
                        + p[i] * p[k + 1] * p[j + 1]
                    )
                    if cost < m_cost[i][j]:
                        m_cost[i][j] = cost
                        s_split[i][j] = k

        # Теперь строим дерево в графе
        graph = nx.Graph()

        def build_tree(i, j):
            # если одна матрица — это лист
            if i == j:
                name = matrices[i]['matrix_name']
                graph.add_node(name)
                return name
            # иначе — создаём узел операции умножения
            k = s_split[i][j]
            node_id = f"mult_{i}_{j}"
            graph.add_node(node_id)
            # левое и правое поддеревья
            left = build_tree(i, k)
            right = build_tree(k + 1, j)
            # соединяем операцию с её аргументами
            graph.add_edge(node_id, left)
            graph.add_edge(node_id, right)
            return node_id

        root = build_tree(0, n - 1)
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

