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
        G = self.P @ b
        n = self.L.shape[0]
        y = np.zeros(n, dtype=self.dtype)
        for i in range(n):
            y[i] = G[i] - self.L[i, :i] @ y[:i]
        x = np.zeros_like(y)
        for i in reversed(range(n)):
            x[i] = (y[i] - self.U[i, i+1:] @ x[i+1:]) / self.U[i, i]
        return x

    def _decompose(self, permute: bool) -> tuple[NDArrayFloat, NDArrayFloat, NDArrayFloat]:
        U = self.A.astype(self.dtype).copy()
        sz = U.shape[0]
        L = np.zeros((sz, sz), self.dtype)
        P = np.eye(sz, dtype=self.dtype)
        for k in range(sz):
            if permute:
                mr = k + np.argmax(np.abs(U[k:, k]))
                if mr != k:
                    U[[k, mr], :] = U[[mr, k], :]
                    P[[k, mr]] = P[[mr, k]]
                    L[[k, mr], :k] = L[[mr, k], :k]
            d = U[k, k]
            if d == 0:
                raise np.linalg.LinAlgError("Zero pivot")
            L[k+1:, k] = U[k+1:, k] / d
            U[k+1:] -= L[k+1:, k, None] * U[k]
        np.fill_diagonal(L, 1.0)
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

