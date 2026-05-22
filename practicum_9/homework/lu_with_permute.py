from abc import ABC, abstractmethod

import numpy as np
from numpy.typing import DTypeLike
from scipy.io import mmread

from practicum_9.lu import LinearSystemSolver
from src.common import NDArrayFloat


class LuSolverWithPermute(LinearSystemSolver):
    
    def __init__(self, A: NDArrayFloat, dtype: DTypeLike, permute: bool) -> None:
        super().__init__(A, dtype)
        self.L, self.U, self.P = self._decompose(permute)


    def solve(self, b: NDArrayFloat) -> NDArrayFloat:
        b = np.asarray(b, dtype=self.dtype)

        n = self.U.shape[0]
        Pb = self.P @ b

        y = np.zeros_like(Pb, dtype=self.dtype)
        for i in range(n):
            y[i] = (Pb[i] - self.L[i, :i] @ y[:i]) / self.L[i, i]

        x = np.zeros_like(y, dtype=self.dtype)
        for i in range(n - 1, -1, -1):
            if np.isclose(self.U[i, i], 0.0):
                raise np.linalg.LinAlgError("Matrix is singular")

            x[i] = (y[i] - self.U[i, i + 1:] @ x[i + 1:]) / self.U[i, i]

        return x


    def _decompose(self, permute: bool) -> tuple[NDArrayFloat, NDArrayFloat, NDArrayFloat]:
        A = np.asarray(self.A, dtype=self.dtype)

        n = A.shape[0]

        U = A.copy()
        L = np.eye(n, dtype=self.dtype)
        P = np.eye(n, dtype=self.dtype)

        for k in range(n - 1):
            if permute:
                pivot = k + np.argmax(np.abs(U[k:, k]))
            else:
                pivot = k

            if np.isclose(U[pivot, k], 0.0):
                raise np.linalg.LinAlgError("Matrix is singular")

            if pivot != k:
                U[[k, pivot], :] = U[[pivot, k], :]

                P[[k, pivot], :] = P[[pivot, k], :]

                if k > 0:
                    L[[k, pivot], :k] = L[[pivot, k], :k]

            for i in range(k + 1, n):
                L[i, k] = U[i, k] / U[k, k]
                U[i, k:] -= L[i, k] * U[k, k:]
                U[i, k] = 0.0

        if np.isclose(U[-1, -1], 0.0):
            raise np.linalg.LinAlgError("Matrix is singular")

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