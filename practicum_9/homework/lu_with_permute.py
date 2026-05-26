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
        n = len(b_permuted)
        y = np.zeros_like(b_permuted)
        
        for i in range(n):
            y[i] = b_permuted[i] - np.dot(self.L[i, :i], y[:i])
        
        x = np.zeros_like(y)
        for i in range(n-1, -1, -1):
            x[i] = (y[i] - np.dot(self.U[i, i+1:], x[i+1:])) / self.U[i, i]
        
        return x

    def _decompose(self, permute: bool) -> tuple[NDArrayFloat, NDArrayFloat, NDArrayFloat]:
        A = self.A.copy().astype(self.dtype)
        n = A.shape[0]
        L = np.eye(n, dtype=self.dtype)
        U = A.copy()
        P = np.eye(n, dtype=self.dtype)
        
        for k in range(n-1):
            if permute:
                pivot_row = np.argmax(np.abs(U[k:, k])) + k
                if pivot_row != k:
                    U[[k, pivot_row]] = U[[pivot_row, k]]
                    P[[k, pivot_row]] = P[[pivot_row, k]]
                    if k > 0:
                        L[[k, pivot_row], :k] = L[[pivot_row, k], :k]
            
            if abs(U[k, k]) < 1e-15:
                raise ValueError("Matrix is singular")
            
            for i in range(k+1, n):
                factor = U[i, k] / U[k, k]
                L[i, k] = factor
                U[i, k:] -= factor * U[k, k:]
        
        return L, U, P


def get_A_b(a_11: float, b_1: float) -> tuple[NDArrayFloat, NDArrayFloat]:
    A = np.array([[a_11, 1.0, -3.0], [6.0, 2.0, 5.0], [1.0, 4.0, -3.0]])
    b = np.array([b_1, 12.0, -39.0])
    return A, b


if __name__ == "__main__":
    p = 16
    a_11 = 3 + 10 ** (-p)
    b_1 = -16 + 10 ** (-p)
    A, b = get_A_b(a_11, b_1)

    solver = LuSolverWithPermute(A, np.float64, permute=True)
    x = solver.solve(b)
    assert np.all(np.isclose(x, [1, -7, 4])), f"The anwser {x} is not accurate enough"
