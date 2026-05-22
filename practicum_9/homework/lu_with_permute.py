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
    
        b_permuted = self.P @ b
        n = self.L.shape[0]

        y = np.zeros_like(b_permuted, dtype=self.dtype)

        for i in range(n):
            y[i] = b_permuted[i] - np.dot(self.L[i, :i], y[:i])

        x = np.zeros_like(y, dtype=self.dtype)

        for i in range(n - 1, -1, -1):
            x[i] = y[i] - np.dot(self.U[i, i+1:], x[i+1:])
            x[i] /= self.U[i, i]

        return x

    def _decompose(self, permute: bool) -> tuple[NDArrayFloat, NDArrayFloat, NDArrayFloat]:
        n = self.A.shape[0]
        U = self.A.copy()
        L = np.eye(n, dtype=self.dtype)
        P = np.eye(n, dtype=self.dtype)

        for k in range(n-1):
            if permute:
                max_index = np.argmax(np.abs(U[k:, k])) + k
                if max_index != k:
                    U[[k, max_index]] = U[[max_index, k]]
                    P[[k, max_index]] = P[[max_index, k]]
                    if k > 0:
                        L[[k, max_index], :k] = L[[max_index, k], :k]
            
            for i in range(k+1, n):
                L[i, k] = U[i, k] / U[k, k]
                U[i, k:] -= L[i, k] * U[k, k:]

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

