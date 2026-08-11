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
        LInv = np.linalg.inv(self.L)
        UInv = np.linalg.inv(self.U)
        P = self.P

        X = UInv @ (LInv @ (P @ b))
        return X

    def _decompose(self, permute: bool) -> tuple[NDArrayFloat, NDArrayFloat, NDArrayFloat]:
        n = self.A.shape[0]
        
        L = np.identity(n, dtype = self.dtype)
        U = self.A.copy()
        P = np.identity(n, dtype = self.dtype)
        
        for k in range(n - 1):
            if permute == True:
                best = k + np.argmax(np.abs(U[k:, k]))
            
                if best != k:
                    L[[k, best], :k] = L[[best, k], :k]
                    U[[k, best]] = U[[best, k]]
                    P[[k, best]] = P[[best, k]]

            if np.isclose(U[k, k], 0):
                raise ValueError("Матрица имеет нулевой определитель!")

            L[k+1:, k] = U[k+1:, k] / U[k, k]
            U[k+1:, k:] -= np.outer(L[k+1:, k], U[k, k:])
        
        return L, U, P



def get_A_b(a_11: float, b_1: float) -> tuple[NDArrayFloat, NDArrayFloat]:
    A = np.array([[a_11, 1.0, -3.0], [6.0, 2.0, 5.0], [1.0, 4.0, -3.0]])
    b = np.array([b_1, 12.0, -39.0])
    return A, b


if __name__ == "__main__":
    p = 16 # modify from 7 to 16 to check instability
    a_11 = 3 + 10 ** (-p)  # add/remove 10**(-p) to check instability
    b_1 = -16 + 10 ** (-p)  # add/remove 10**(-p) to check instability
    A, b = get_A_b(a_11, b_1)

    solver = LuSolverWithPermute(A, np.float64, permute=True)
    x = solver.solve(b)
    print(x)
    assert np.all(np.isclose(x, [1, -7, 4])), f"The anwser {x} is not accurate enough"

