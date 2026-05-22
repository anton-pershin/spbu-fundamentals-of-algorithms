from abc import ABC, abstractmethod

import numpy as np
from numpy.typing import DTypeLike

from practicum_9.lu import LinearSystemSolver
from src.common import NDArrayFloat


class LuSolverWithPermute(LinearSystemSolver):
    def __init__(self, A: NDArrayFloat, dtype: DTypeLike, permute: bool) -> None:
        super().__init__(A, dtype)
        self.L, self.U, self.P = self._decompose(permute)

    def solve(self, b: NDArrayFloat) -> NDArrayFloat:

        b = self.P @ b.copy()
        n = len(b)
        y = np.zeros(n, dtype=self.dtype)

        for i in range(n):
            y[i] = b[i]
            for j in range(i):
                y[i] -= self.L[i, j] * y[j]

        x = np.zeros(n, dtype=self.dtype)

        for i in range(n - 1, -1, -1):
            x[i] = y[i]

            for j in range(i + 1, n):
                x[i] -= self.U[i, j] * x[j]
                
            x[i] /= self.U[i, i]

        return x

    def _decompose(self, permute: bool) -> tuple[NDArrayFloat, NDArrayFloat, NDArrayFloat]:

        n = self.A.shape[0]
        L = np.eye(n, dtype=self.dtype)
        U = self.A.copy().astype(self.dtype)
        P = np.eye(n, dtype=self.dtype)

        for k in range(n - 1):
            if permute:
                max_row = np.argmax(np.abs(U[k:, k])) + k

                if max_row != k:
                    U[[k, max_row]] = U[[max_row, k]]
                    P[[k, max_row]] = P[[max_row, k]]

                    if k > 0:
                        L[[k, max_row], :k] = L[[max_row, k], :k]
            # for i in range(k + 1, n):
            #     L[i, k] = U[i, k] / U[k, k]
            #     for j in range(k, n):
            #         U[i, j] = U[i, j] - L[i, k] * U[k, j]
            if np.abs(U[k, k]) < 1e-15:
                raise ValueError("Zero pivot element")
            L[k+1:, k] = U[k+1:, k] / U[k, k]
            U[k+1:, k:] -= np.outer(L[k+1:, k], U[k, k:])

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