from abc import ABC, abstractmethod

import numpy as np

from numpy.typing import DTypeLike

from practicum_9.lu import LinearSystemSolver
from src.common import NDArrayFloat


class LuSolverWithPermute(LinearSystemSolver):
    def __init__(self, A: NDArrayFloat, dtype: DTypeLike, permute: bool) -> None:
        super().__init__(A, dtype)
        self.L, self.U, self.P = self._decompose(permute)

    def _decompose(self, permute: bool) -> tuple[NDArrayFloat, NDArrayFloat, NDArrayFloat]:
        n = self.A.shape[0]
        U = self.A.astype(self.dtype).copy()
        L = np.eye(n, dtype=self.dtype)
        P = np.eye(n, dtype=self.dtype)

        for i in range(n):
            if permute:
                # Выбор главного элемента: ищем индекс максимального в столбце
                pivot = np.argmax(np.abs(U[i:, i])) + i
                # Меняем строки в U, L (до i) и P
                U[[i, pivot]] = U[[pivot, i]]
                P[[i, pivot]] = P[[pivot, i]]
                if i > 0:
                    L[[i, pivot], :i] = L[[pivot, i], :i]

            for j in range(i + 1, n):
                factor = U[j, i] / U[i, i]
                L[j, i] = factor
                U[j, i:] -= factor * U[i, i:]

        return L, U, P

    def solve(self, b: NDArrayFloat) -> NDArrayFloat:
        # Умножаем b на матрицу перестановок P
        b_permuted = self.P @ b

        # 1. Ly = Pb (прямая подстановка)
        y = np.zeros_like(b_permuted)
        for i in range(len(b)):
            y[i] = b_permuted[i] - self.L[i, :i] @ y[:i]

        # 2. Ux = y (обратная подстановка)
        x = np.zeros_like(y)
        for i in range(len(y) - 1, -1, -1):
            x[i] = (y[i] - self.U[i, i + 1:] @ x[i + 1:]) / self.U[i, i]

        return x


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

