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
        b = self.P @ b
        y = np.zeros(n)
        x = np.zeros(n)
        
        for i in range(n):
            s = 0

            for j in range(i):
                s += self.L[i][j] * y[j]
            y[i] = b[i] - s

        for i in range(n - 1, -1, -1):
            s = 0

            for j in range(i + 1, n):
                s += self.U[i][j] *x[j]

            x[i] = (y[i] - s) / self.U[i][i]

        return x

    def _decompose(self, permute: bool) -> tuple[NDArrayFloat, NDArrayFloat, NDArrayFloat]:

        n = self.A.shape[0]
        L = np.eye(n)
        U = self.A.copy()
        P = np.eye(n)

        for k in range(n):

            if permute:
                max_row = k

                for i in range(k + 1, n):
                    if abs(U[i][k]) > abs(U[max_row][k]):
                        max_row = i

                if max_row != k:
                    U[[k, max_row]] = U[[max_row, k]]
                    P[[k, max_row]] = P[[max_row, k]]

                if k > 0:
                    L[[k, max_row], :k] = L[[max_row, k], :k]

            for i in range(k + 1, n):
                multiplier = U[i][k] / U[k][k]
                L[i][k] = multiplier

                for j in range(k, n):
                    U[i][j] = U[i][j] - multiplier * U[k][j]

        return L, U, P
                    
def get_A_b(a_11: float, b_1: float) -> tuple[NDArrayFloat, NDArrayFloat]:
    A = np.array([[a_11, 1.0, -3.0], [6.0, 2.0, 5.0], [1.0, 4.0, -3.0]])
    b = np.array([b_1, 12.0, -39.0])
    return A, b

if __name__ == "__main__":
    for p in range(7, 17):
        a_11 = 3 + 10 ** (-p)
        b_1 = -16 + 10 ** (-p)
        A, b = get_A_b(a_11, b_1)
                
        solver = LuSolverWithPermute(A, np.float64, permute=True)
        x = solver.solve(b)
                
        if np.all(np.isclose(x, [1, -7, 4])):
            print(f"p={p}: good: {x}")
        else:
            print(f"p={p}: not accurate! got: {x}")
