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
        if self.P is not None:
            b = self.P @ b

        y = np.zeros_like(b, dtype=self.dtype)
        for i in range(len(b)):
            y[i] = (b[i] - np.dot(self.L[i, :i], y[:i])) / self.L[i, i]

        x = np.zeros_like(b, dtype=self.dtype)
        for i in range(len(b) - 1, -1, -1):
            x[i] = (y[i] - np.dot(self.U[i, i+1:], x[i+1:])) / self.U[i, i]

        return x

    def _decompose(self, permute: bool) -> tuple[NDArrayFloat, NDArrayFloat, NDArrayFloat]:
        n = self.A.shape[0]
        A = self.A.copy()
        L = np.eye(n, dtype=self.dtype)
        P = np.eye(n, dtype=self.dtype) if permute else None

        for k in range(n):
            if permute:
                max_idx = np.argmax(np.abs(A[k:, k])) + k
                if max_idx != k:
                    A[[k, max_idx]] = A[[max_idx, k]]
                    L[[k, max_idx], :k] = L[[max_idx, k], :k]

                    if P is not None:
                        P[[k, max_idx]] = P[[max_idx, k]]

            if np.abs(A[k, k]) < 1e-12:
                raise np.linalg.LinAlgError("Singular matrix")

            for i in range(k + 1, n):
                L[i, k] = A[i, k] / A[k, k]
                A[i, :] = A[i, :] - L[i, k] * A[k, :]

        U = np.triu(A)
        if not permute:
            P = None

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

    print("Solution x:", x)
    print("A @ x:", A @ x)
    print("b:", b)
    assert np.all(np.isclose(x, [1, -7, 4])), f"The answer {x} is not accurate enough"