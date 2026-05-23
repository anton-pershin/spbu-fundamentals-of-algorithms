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
        b = b.astype(self.dtype)
        Pb = self.P @ b
        y = np.zeros(n, dtype=self.dtype)

        for i in range(n):
            y[i] = Pb[i] - np.dot(self.L[i, :i], y[:i])

        x = np.zeros(n, dtype=self.dtype)
        for i in range(n-1, -1, -1):
            if self.U[i, i] == 0:
                raise ValueError("Zero pivot encountered during back substitution.")
            x[i] = (y[i] - np.dot(self.U[i, i+1:], x[i+1:])) / self.U[i, i]

        return x

    def _decompose(self, permute: bool) -> tuple[NDArrayFloat, NDArrayFloat, NDArrayFloat]:

        n = self.A.shape[0]
        L = np.identity(n, dtype=self.dtype)
        U = self.A.copy().astype(self.dtype)
        P = np.identity(n, dtype=self.dtype)

        if not permute:
            for k in range(n-1):
                if U[k, k] == 0:
                    raise ValueError("Zero pivot encountered. Consider using pivoting.")
                L[k+1:, k] = U[k+1:, k] / U[k, k]
                U[k+1:, k:] -= np.outer(L[k+1:, k], U[k, k:])
            return L, U, P

        for k in range(n-1):
            pivot = k + int(np.argmax(np.abs(U[k:, k])))
            if np.abs(U[pivot, k]) < 1e-18:
                raise ValueError("Zero pivot encountered even after pivoting.")

            if pivot != k:
                U[[k, pivot], :] = U[[pivot, k], :]
                P[[k, pivot], :] = P[[pivot, k], :]
                if k > 0:
                    L[[k, pivot], :k] = L[[pivot, k], :k]

            L[k+1:, k] = U[k+1:, k] / U[k, k]
            U[k+1:, k:] -= np.outer(L[k+1:, k], U[k, k:])

        return L, U, P


def get_A_b(a_11: float, b_1: float) -> tuple[NDArrayFloat, NDArrayFloat]:
    A = np.array([[a_11, 1.0, -3.0], [6.0, 2.0, 5.0], [1.0, 4.0, -3.0]])
    b = np.array([b_1, 12.0, -39.0])
    return A, b


if __name__ == "__main__":
    p = 7  # modify from 7 to 16 to check instability
    a_11 = 3 + 10 ** (-p)  # add/remove 10**(-p) to check instability
    b_1 = -16 + 10 ** (-p)  # add/remove 10**(-p) to check instability
    A, b = get_A_b(a_11, b_1)

    solver = LuSolverWithPermute(A, np.float64, permute=True)
    x = solver.solve(b)
    print(x)
    assert np.all(np.isclose(x, [1, -7, 4])), f"The anwser {x} is not accurate enough"

