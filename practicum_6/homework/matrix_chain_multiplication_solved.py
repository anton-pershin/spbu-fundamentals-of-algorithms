
#
# Матрица A_i имеет размер p[i-1] x p[i].
#  Массив p имеет длину n+1.
#
#
# dp[i][j] = минимальная стоимость умножения [ A_i ... A_j ]
#
# dp[i][j] = min { dp[i][k] + dp[k+1][j] + p[i-1]*p[k]*p[j] }
#
# dp[i][i] = 0
#
#
# s – "split" (точка разбиения).
# s[i][j] хранит k, при котором dp[i][j]
#  достиг минимума.
#
#
# Как перебирать i, j.
#
#  dp[i][j] зависит от dp[i][k] и dp[k+1][j]
#
#  Вычисления dp[][] и p[][] для более коротких
#   цепочек используются в вычислениях более длинных.
#
#  Перебираем по длине цепочки:
#   length=1: dp[1][1] , ...              , dp[n][n] = 0
#   length=2: dp[1][2] , ... , dp[n-1][n]
#   ...
#   length=n: dp[1][n]  -> ответ
#
#
# Как вырастить дерево.
#
#  Рекурсивно, сверху вниз.
#   Если s[1][n] == k, то последнее умножение == 
#    (A_1 ... A_k) * (A_{k+1} ... A_n)
#
#             [1..n]
#            /      \
#        [1..k]   [k+1..n]
#        /    \
#      [1..k'] [k'+1..k]
#      /   \
#     A_1  A_2
#
#  Восстанавливаем умножения снизу вверх.
#


from pathlib import Path
from typing import Any, Union

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx

from src.common import AnyNxGraph


class MatrixChainMultiplication:

    def __init__(self) -> None:
        pass

    def run(self, matrices: list[
        dict[ str, str | tuple[int, int] ]
    ]) -> tuple[AnyNxGraph, Any]:

        n = len(matrices)

        # A_i:     p[i-1] x p[i]
        # длина p: n+1.
        p = [ mat["shape"][0] for mat in matrices ]
        p.append(matrices[-1]["shape"][1])

        # dp, s:   [n+1] x [n+1]
        # индексы: 0 ... n
        dp = [ (n + 1) * [0] for _ in range(n + 1) ]
        s  = [ (n + 1) * [0] for _ in range(n + 1) ]

        # Предвычисляем таблицы для
        #  стоимостей и позиций k:

        # length: [2 .. n]
        for length in range(2, n + 1):
            # i: [1 .. n+1 - length] < [1 .. n-1]
            for i in range(1, n + 2 - length):
                # j: { j - i == length - 1 }
                j = i - 1 + length
                dp[i][j] = float("inf")
                for k in range(i, j):
                    cost = (
                        dp[i][k]
                        + dp[k + 1][j]
                        + p[i-1] * p[k] * p[j]
                    )
                    if cost < dp[i][j]:
                        dp[i][j] = cost
                        s[i][j]  = k

        # Рекурсивно строим дерево
        #  по таблице s[][]:

        tree = nx.DiGraph()
        counter = 0

        def build_subtree(i: int, j: int) -> Any:

            nonlocal counter

            if i == j:
                # База рекурсии:
                #  одна матрица (лист дерева)
                name = matrices[i - 1]["matrix_name"]
                tree.add_node(name)
                return name

            # Рекурсия расщепляет [i..j] на два куска
            #  и возвращает id корня каждого поддерева.
            #
            #        build_subtree(i, j)
            #               |
            #         k = s[i][j]
            #            /     \
            #       [i..k]   [k+1..j]
            #         |          |
            #        left      right        #!
            #            \     /
            #            node_id            #!

            k     = s[i][j]
            left  = build_subtree(i, k)     #!
            right = build_subtree(k + 1, j) #!

            node_id = counter
            counter += 1

            tree.add_node(node_id)

            tree.add_edge(node_id, left)   #!
            tree.add_edge(node_id, right)  #!

            return node_id                 #!

        root_id = build_subtree(1, n)

        return tree, root_id


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

    mcm            = MatrixChainMultiplication()
    matmul_tree, _ = mcm.run(test_matrices)

    out_dir = Path("practicum_6/homework/plot")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    pos = nx.spring_layout(matmul_tree, seed=42)
    nx.draw_networkx(matmul_tree, pos, node_color="white", edgecolors="black")
    plt.savefig(out_dir / "matmul_tree.png", bbox_inches="tight")
    plt.close()
