
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))


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
        n = self.U.shape[0]

        # solving for y
        y = np.zeros(n, dtype=self.dtype)
        for i in range(n):  # iterating by rows...
            y[i] = b[self.P[i]]  # adjust B by permutation
            for j in range(i):  # ...and by cols
                y[i] -= self.L[i][j] * y[j]
                # no need for y[i] /= ... as L contains 1 on the main diagonal :)

        # for x
        x = np.zeros(n, dtype=self.dtype)
        for i in range(n - 1, -1, -1):  # 'backwards' as its UPPER triag matrix :)
            x[i] = y[i]
            for j in range(i + 1, n):
                x[i] -= self.U[i][j] * x[j]
            x[i] /= self.U[i][i]  # getting rid of constant before x

        return x
        

    def _decompose(self, permute: bool) -> tuple[NDArrayFloat, NDArrayFloat, NDArrayFloat]:
        n = self.A.shape[0]
        L = np.eye(n, dtype=self.dtype)
        U = self.A.copy()
        P = np.arange(n)  # array of indices that determine row swaps

        for k in range(n):  # k = column
            if permute:
                pivot = np.argmax(np.abs(U[k:n, k])) + k  # '+ k' to make the index absolute (not replative to the submatrix with rows k to n)
                if pivot != k:
                    U[[k, pivot], :] = U[[pivot, k], :]
                    L[[k, pivot], :k] = L[[pivot, k], :k]
                    P[[k, pivot]] = P[[pivot, k]]

            for i in range(k + 1, n):
                
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
    
    matrices = {
        'P': np.array([np.eye(solver.U.shape[0], dtype=np.float64)[i] for i in solver.P]),
        'L': solver.L,
        'U': solver.U,
    }
    
    x = solver.solve(b)
    print(x)
    
    assert np.all(np.isclose(x, [1, -7, 4])), f"The answer {x} is not accurate enough"
    



