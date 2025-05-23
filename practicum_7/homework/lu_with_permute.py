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
        # Прямой ход: решаем Ly = Pb
        Pb = self.P @ b
        y = np.zeros_like(b, dtype=self.dtype)
        n = self.L.shape[0]
        for i in range(n):
            y[i] = Pb[i] - np.dot(self.L[i, :i], y[:i])
        # Обратный ход: решаем Ux = y
        x = np.zeros_like(b, dtype=self.dtype)
        for i in reversed(range(n)):
            x[i] = (y[i] - np.dot(self.U[i, i+1:], x[i+1:])) / self.U[i, i]
        return x

    def _decompose(self, permute: bool) -> tuple[NDArrayFloat, NDArrayFloat, NDArrayFloat]:
        A = self.A.astype(self.dtype).copy()
        n = A.shape[0]
        L = np.zeros((n, n), dtype=self.dtype)
        U = A.copy()
        P = np.eye(n, dtype=self.dtype)

        for k in range(n):
            if permute:
                # Находим индекс строки с максимальным элементом в столбце k начиная с k
                max_row = np.argmax(np.abs(U[k:, k])) + k
                if max_row != k:
                    # Переставляем строки в U
                    U[[k, max_row], :] = U[[max_row, k], :]
                    # Переставляем строки в P
                    P[[k, max_row], :] = P[[max_row, k], :]
                    # Переставляем строки в L (только до k столбца)
                    if k > 0:
                        L[[k, max_row], :k] = L[[max_row, k], :k]
            # Строим L и U
            for i in range(k+1, n):
                if U[k, k] == 0:
                    raise np.linalg.LinAlgError("Zero pivot encountered.")
                L[i, k] = U[i, k] / U[k, k]
                U[i, :] = U[i, :] - L[i, k] * U[k, :]
        # Заполняем диагональ L единицами
        for i in range(n):
            L[i, i] = 1.0
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
    assert np.all(np.isclose(x, [1, -7, 4])), f"The anwser {x} is not accurate enough"

