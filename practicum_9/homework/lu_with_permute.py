import sys
from pathlib import Path

root_path = Path(__file__).resolve().parents[2]
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))

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
        n = self.L.shape[0]
        bp = np.dot(self.P, b)
        
        y = np.zeros(n, dtype=self.dtype)
        for i in range(n):
            val = bp[i]
            for j in range(i):
                val -= self.L[i, j] * y[j]
            y[i] = val

        x = np.zeros(n, dtype=self.dtype)
        for i in range(n - 1, -1, -1):
            val = y[i]
            for j in range(i + 1, n):
                val -= self.U[i, j] * x[j]
            x[i] = val / self.U[i, i]

        return x

    def _decompose(self, permute: bool) -> tuple[NDArrayFloat, NDArrayFloat, NDArrayFloat]:
        A_curr = self.A.astype(self.dtype).copy()
        n = A_curr.shape[0]
        P = np.eye(n, dtype=self.dtype)

        for k in range(n):
            if permute:
                pivot = k
                for r in range(k + 1, n):
                    if abs(A_curr[r, k]) > abs(A_curr[pivot, k]):
                        pivot = r
                if pivot != k:
                    A_curr[[k, pivot]] = A_curr[[pivot, k]]
                    P[[k, pivot]] = P[[pivot, k]]

            for i in range(k + 1, n):
                factor = A_curr[i, k] / A_curr[k, k]
                A_curr[i, k] = factor
                for j in range(k + 1, n):
                    A_curr[i, j] -= factor * A_curr[k, j]

        L = np.eye(n, dtype=self.dtype)
        U = np.zeros((n, n), dtype=self.dtype)
        for i in range(n):
            for j in range(n):
                if i > j:
                    L[i, j] = A_curr[i, j]
                else:
                    U[i, j] = A_curr[i, j]

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
    assert np.all(np.isclose(x, [1, -7, 4])), f"The answer {x} is not accurate enough"