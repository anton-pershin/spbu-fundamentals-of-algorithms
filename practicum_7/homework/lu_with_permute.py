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
        b_permuted = self.P @ b
        y = np.zeros_like(b_permuted)
        for i in range(len(b)):
            y[i] = b_permuted[i] - np.dot(self.L[i, :i], y[:i])
        x = np.zeros_like(y)
        for i in reversed(range(len(b))):
            x[i] = (y[i] - np.dot(self.U[i, i + 1:], x[i + 1:])) / self.U[i, i]
        return x

    def _decompose(self, permute: bool) -> tuple[NDArrayFloat, NDArrayFloat, NDArrayFloat]:
        A = self.A.copy()
        n = A.shape[0]
        L = np.eye(n, dtype=A.dtype)
        U = A.copy()
        P = np.eye(n, dtype=A.dtype)
        for i in range(n):
            if permute:
                max_row = np.argmax(np.abs(U[i:, i])) + i
                if max_row != i:
                    U[[i, max_row], :] = U[[max_row, i], :]
                    P[[i, max_row], :] = P[[max_row, i], :]
                    if i > 0:
                        L[[i, max_row], :i] = L[[max_row, i], :i]
            for j in range(i + 1, n):
                multiplier = U[j, i] / U[i, i]
                L[j, i] = multiplier
                U[j] = U[j] - multiplier * U[i]
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
