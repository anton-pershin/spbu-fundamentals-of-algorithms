from abc import ABC, abstractmethod

import numpy as np
from numpy.typing import DTypeLike

from practicum_7.lu import LinearSystemSolver
from src.common import NDArrayFloat


class LuSolverWithPermute(LinearSystemSolver):
    def __init__(self, A: NDArrayFloat, dtype: DTypeLike, permute: bool) -> None:
        super().__init__(A, dtype)
        self.L, self.U, self.P = self._decompose(permute)

    def solve(self, b: NDArrayFloat) -> NDArrayFloat:
        n = len(b)
        b_permuted = np.dot(self.P, b)  # преобразуем правую часть LUx = P * b

        y = np.zeros(n, dtype=self.dtype) # решаем Ly = Pb
        for i in range(n):
            summ = 0
            for j in range(i):
                summ += self.L[i][j] * y[j]
            y[i] = b_permuted[i] - summ

        x = np.zeros(n, dtype=self.dtype) # находим Ux = y
        for i in reversed(range(n)):
            summ = 0
            for j in range(i + 1, n):
                summ += self.U[i][j] * x[j]
            x[i] = (y[i] - summ) / self.U[i][i]

        return x

    def _decompose(self, permute: bool) -> tuple[NDArrayFloat, NDArrayFloat, NDArrayFloat]:
        A = self.A.copy() # в стандартных обозначениях это U
        n = len(A)
        L = np.eye(n)
        P = np.eye(n)
        for k in range(n): # k-тый шаг метода Гаусса
            if (permute):
                pivot_index = np.argmax(np.abs(A[k:, k])) + k
                if pivot_index != k: 
                    A[[k, pivot_index], :] = A[[pivot_index, k], :] # переставляем строки в A
                    P[[k, pivot_index], :] = P[[pivot_index, k], :] # переставляем строки в P
                    L[[k, pivot_index], :k] = L[[pivot_index, k], :k] # переставляем строки L - только левую часть до текущего k
            for i in range(k + 1, n):
                m_ik = A[i][k] / A[k][k]
                L[i][k] = m_ik                
                for j in range(k, n):
                    A[i][j] -= m_ik * A[k][j]
        return L, A, P


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
    assert np.all(np.isclose(x, [1, -7, 4])), f"The anwser {x} is not accurate enough"

