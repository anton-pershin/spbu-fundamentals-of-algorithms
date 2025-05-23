import sys
from pathlib import Path
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

from abc import ABC, abstractmethod

import numpy as np
from numpy.typing import DTypeLike

from practicum_7.lu import LinearSystemSolver
from src.common import NDArrayFloat


class LuSolverWithPermute(LinearSystemSolver):
    def __init__(self, A: NDArrayFloat, dtype: DTypeLike, permute: bool) -> None:
        super().__init__(A, dtype)
        self.L, self.U, self.P = self._decompose(permute)

    def solve(self, B: NDArrayFloat) -> NDArrayFloat:
        """
        Решает систему AX = B, используя LU-разложение
        P - матрица перестановок
        PA = LU  ===>  LU * X = PB
        Алгоритм:
        1) Вычислить B_perm = PB
        2) Решить LY = B_perm (прямой ход)
        3) Решить UX = Y (обратный ход)
        """

        # Применяем перестановки к вектору правой части
        B_perm = self.P @ B # @ - оператор матричного умножения
        n = B_perm.shape[0]
        # Прямой ход: LY = B_perm
        Y = np.zeros_like(B_perm)
        for i in range(n):
            Y[i] = B_perm[i] - np.dot(self.L[i, :i], Y[:i])
        # Обратный ход: UX = Y
        X = np.zeros_like(Y)
        for i in range(n - 1, -1, -1):
            X[i] = (Y[i] - np.dot(self.U[i, i + 1:], X[i + 1:])) / self.U[i, i]
        return X

    def _decompose(self, permute: bool) -> tuple[NDArrayFloat, NDArrayFloat, NDArrayFloat]:
        """
        Выполняет LU-разложение матрицы A (из базового класса) с частичным выбором главного элемента,
        если permute=True.
        Возвращает L, U, P, причем PA = LU
        """
        A = self.A.astype(self.dtype)  # копируем A в нужном типе
        n = A.shape[0]
        # Инициализируем P как единичную матрицу перестановок
        P = np.eye(n, dtype=self.dtype)
        # U начально копия A, L — нулевая с единицами на диагонали
        U = A.copy()
        L = np.eye(n, dtype=self.dtype)

        for i in range(n):
            if permute:
                # Находим в столбце i максимальный по модулю элемент в строках i..n-1
                pivot = np.argmax(np.abs(U[i:, i])) + i
                # Если нужно — меняем строки i и pivot в U и P, и соответствующие части L
                if pivot != i:
                    U[[i, pivot], :] = U[[pivot, i], :]
                    P[[i, pivot], :] = P[[pivot, i], :]
                    # В L нужно поменять элементы в столбцах [0..i-1]
                    if i > 0:
                        L[[i, pivot], :i] = L[[pivot, i], :i]
            # Теперь делаем "нормализацию" и заносим множители в L
            for j in range(i + 1, n):
                factor = U[j, i] / U[i, i]
                L[j, i] = factor
                # Вычитаем из строки j: factor * строка i
                U[j, :] -= factor * U[i, :]
        return L, U, P

def get_A_b(a_11: float, b_1: float) -> tuple[NDArrayFloat, NDArrayFloat]:
    A = np.array([[a_11, 1.0, -3.0], [6.0, 2.0, 5.0], [1.0, 4.0, -3.0]])
    b = np.array([b_1, 12.0, -39.0])
    return A, b


if __name__ == "__main__":
    p = 16  # modify from 7 to 16 to check instability
    a_11 = 3 + 10 ** (-p)  # add/remove 10**(-p) to check instability
    b_1 = -16 + 10 ** (-p)  # add/remove 10**(-p) to check instability
    A, b = get_A_b(a_11, b_1)

    solver = LuSolverWithPermute(A, np.float64, permute=True)
    x = solver.solve(b)
    print("X: ", x)
    assert np.all(np.isclose(x, [1, -7, 4])), f"The anwser {x} is not accurate enough"

