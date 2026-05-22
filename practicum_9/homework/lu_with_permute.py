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
        n = self.A.shape[0]

        # P - permute, L - low trian, U - up trian, A - matrix, x - unknown, b - right part
        # Ax = b ---[PA = LU]---[PAx = Pb]---> LUx = Pb ---> Ly = Pb где y = Ux:

        pb = self.P @ b # if permute false P * b = b
        y = np.zeros(n, dtype=self.dtype)
        for i in range(n):
            y[i] = pb[i] - np.sum(self.L[i, :i] * y[:i])

        x = np.zeros(n, dtype=self.dtype)
        for i in range(n - 1, -1, -1):
            x[i] = (y[i] - np.sum(self.U[i, i + 1:] * x[i + 1:])) / self.U[i, i]
        return x

    def _decompose(self, permute: bool) -> tuple[NDArrayFloat, NDArrayFloat, NDArrayFloat]:
        n = self.A.shape[0]
        U = self.A.copy()
        L = np.eye(n, dtype=self.dtype)
        P = np.eye(n, dtype=self.dtype)

        for k in range(n - 1):
            if permute:
                pivot_row = np.argmax(np.abs(U[k:, k])) + k
                if pivot_row != k:
                    U[[k, pivot_row]] = U[[pivot_row, k]]
                    P[[k, pivot_row]] = P[[pivot_row, k]]
                    if k > 0:
                        L[[k, pivot_row], :k] = L[[pivot_row, k], :k]

            if np.abs(U[k, k]) < 1e-12:
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

