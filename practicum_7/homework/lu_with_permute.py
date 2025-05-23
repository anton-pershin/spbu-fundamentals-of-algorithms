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
        
        Pb = np.dot(self.P, b) #для учета перестановок
        n = len(b)
        y = np.zeros_like(b, dtype=self.dtype)
        for i in range(n):
            y[i] = Pb[i] - np.dot(self.L[i, :i], y[:i])
        x = np.zeros_like(y, dtype=self.dtype)
        
        for i in range(n - 1, -1, -1):
            x[i] = (y[i] - np.dot(self.U[i, i + 1:], x[i + 1:])) / self.U[i, i]
        
        return x

    def _decompose(self, permute: bool) -> tuple[NDArrayFloat, NDArrayFloat, NDArrayFloat]:
        
        n = self.A.shape[0]
        L = np.zeros((n, n), dtype=self.dtype)
        U = np.array(self.A, copy=True, dtype=self.dtype)
        P = np.eye(n, dtype=self.dtype) 

        for k in range(n):
            if permute:
                max_row_index = np.argmax(np.abs(U[k:n, k])) + k
                if max_row_index != k:
                    U[[k, max_row_index]] = U[[max_row_index, k]]
                    P[[k, max_row_index]] = P[[max_row_index, k]]
                    if k > 0:
                        L[[k, max_row_index], :k] = L[[max_row_index, k], :k]

            for i in range(k + 1, n):
                L[i, k] = U[i, k] / U[k, k]
                U[i, k:n] -= L[i, k] * U[k, k:n]

        np.fill_diagonal(L, 1) #заполнение диагонали
        
        return L, U, P


def get_A_b(a_11: float, b_1: float) -> tuple[NDArrayFloat, NDArrayFloat]:
    A = np.array([[a_11, 1.0, -3.0],
                  [6.0, 2.0, 5.0],
                  [1.0, 4.0, -3.0]])
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