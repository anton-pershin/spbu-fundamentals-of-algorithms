from pathlib import Path
from typing import Any, Union

import numpy as np
import networkx as nx

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph

class MatrixChainMultiplication:
    def __init__(self) -> None:
        
        self.graph = nx.Graph() #для дерева умножения
        self.matrices = [] #список матриц
        self.n = 0 #кол-во матриц
        self.dimensions = [] #размерность м
        self.dp = [] #для хранения min числовых операций подмасивов матриц
        self.splits = [] #хр индекс оптамальное разбиение

    def run( #принимает список матриц имен и  размера
        self,
        matrices: list[dict[str, Union[str, tuple[int, int]]]]
    ) -> tuple[AnyNxGraph, Any]:
        
        self.matrices = matrices #сох-т список м в обьекте
        self.n = len(self.matrices) # кол-во эл-в в матрицах

        self.dimensions = [self.matrices[i]['shape'][0] for i in range(self.n)] + [self.matrices[-1]['shape'][1]]

        self.dp = [[0] * self.n for _ in range(self.n)] #min число операций для перем м от i до j
        self.splits = [[0] * self.n for _ in range(self.n)] #хранит индекс где происход оптимал разложение

        for length in range(2, self.n + 1): #алг для нахожд оптимал порядка
            for i in range(self.n - length + 1):
                j = i + length - 1 #i-начало j-конеу
                self.dp[i][j] = float('inf') #чтобы найти min эл-т
                for k in range(i, j): #определяет границу где проход разбиение
                    # умноден матриц
                    q = self.dp[i][k] + self.dp[k + 1][j] + self.dimensions[i] * self.dimensions[k + 1] * self.dimensions[j + 1]
                    if q < self.dp[i][j]:
                        self.dp[i][j] = q
                        self.splits[i][j] = k

        #строение дерева
        def build_tree(i: int, j: int) -> Any: 
            
            if i == j: #если цепочка из 1 матрицу
                return self.matrices[i]['matrix_name']

            k = self.splits[i][j] #сторим левое в иправое поддеревя
            left = build_tree(i, k)
            right = build_tree(k + 1, j)
            self.graph.add_edge(left, right, weight=1) #добавляем ребро между графами
            return f"({left} x {right})" #возр стРОковое умножен

        root = build_tree(0, self.n - 1) #строим дерево для всей цепочки мат
        return self.graph, root #возр граф и корень дерева


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