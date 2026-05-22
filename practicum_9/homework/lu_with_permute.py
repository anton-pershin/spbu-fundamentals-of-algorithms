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
        b_cast = b.astype(self.dtype)

        b_permuted = self.P @ b_cast

        n = self.L.shape[0]

        y = np.zeros(n, dtype=self.dtype)
        for i in range(n):
            y[i] = b_permuted[i] - np.dot(self.L[i,:i],y[:i])

        x = np.zeros(n,dtype=self.dtype)
        for i in range(n-1,-1,-1):
            x[i] = (y[i] - np.dot(self.U[i,i+1:],x[i+1:])) / self.U[i,i]
        return x

    def _decompose(self, permute: bool) -> tuple[NDArrayFloat, NDArrayFloat, NDArrayFloat]:
        n = self.A.shape[0]

        LU = self.A.copy()

        P = np.eye(n, dtype=self.dtype)

        for k in range(n-1):
            if permute:
                pivotRow = k + np.argmax(np.abs(LU[k:,k]))
                if pivotRow != k:
                    LU[[k,pivotRow],:] = LU[[pivotRow,k],:]

                    P[[k,pivotRow], :] = P[[pivotRow,k],:]
            if LU[k,k] == 0:
                raise ValueError("zero element")
            LU[k+1:, k] /= LU[k,k]
            LU[k+1:,k+1:] -= np.outer(LU[k+1:,k],LU[k,k+1:])
        
        L = np.tril(LU,k=-1) + np.eye(n,dtype=self.dtype)
        
        U = np.triu(LU)

        return L,U,P


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

