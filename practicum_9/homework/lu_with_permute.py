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

        y = np.linalg.solve(self.L, self.P @ b)
        x = np.linalg.solve(self.U, y)
        return x

    def _decompose(self, permute: bool) -> tuple[NDArrayFloat, NDArrayFloat, NDArrayFloat]:

        n = len(self.A)
        U = self.A.copy().astype(float)
        L = np.eye(n)
        P = np.eye(n)

        for k in range(n - 1):
            if permute:
                max_idx = np.argmax(np.abs(U[k:, k])) + k
                if max_idx != k:
                    U[[k, max_idx]] = U[[max_idx, k]]
                    L[[k, max_idx], :k] = L[[max_idx, k], :k]
                    P[[k, max_idx]] = P[[max_idx, k]]

            for i in range(k + 1, n):
                factor = U[i, k] / U[k, k]
                L[i,k] = factor
                U[i, k:] -= factor * U[k, k:]

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

