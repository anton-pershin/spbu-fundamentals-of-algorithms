import numpy as np

from abc import ABC, abstractmethod
from numpy.typing import DTypeLike

from practicum_9.lu import LinearSystemSolver
from src.common import NDArrayFloat

class LuSolverWithPermute(LinearSystemSolver):
    def __init__(self, A: NDArrayFloat, dtype: DTypeLike, permute: bool) -> None:
        super().__init__(A, dtype)
        self.L, self.U, self.P = self._decompose(permute)

    def solve(self, b: NDArrayFloat) -> NDArrayFloat:
        Pb = self.P @ b
        n = len(Pb)
        
        y = np.zeros_like(Pb, dtype=self.dtype)
        for i in range(n):
            y[i] = Pb[i] - sum(self.L[i, j] * y[j] for j in range(i))
        
        x = np.zeros_like(Pb, dtype=self.dtype)
        for i in range(n - 1, -1, -1):
            x[i] = (y[i] - sum(self.U[i, j] * x[j] for j in range(i + 1, n))) / self.U[i, i]
        
        return x

    def _decompose(self, permute: bool) -> tuple[NDArrayFloat, NDArrayFloat, NDArrayFloat]:
        A = self.A.copy().astype(self.dtype)
        n = A.shape[0]
        
        L = np.eye(n, dtype=self.dtype)
        U = A.copy()
        P = np.eye(n, dtype=self.dtype)
        
        for k in range(n - 1):
            if permute:
                max_idx = np.argmax(np.abs(U[k:, k]))
                max_row = k + max_idx
                
                if max_row != k:
                    U[[k, max_row]] = U[[max_row, k]]
                    P[[k, max_row]] = P[[max_row, k]]
                    if k > 0:
                        L[[k, max_row], :k] = L[[max_row, k], :k]
            
            if np.abs(U[k, k]) < 1e-12:
                raise ValueError(f"Матрица вырождена на шаге {k}")
            
            for i in range(k + 1, n):
                factor = U[i, k] / U[k, k]
                L[i, k] = factor
                U[i, k:] -= factor * U[k, k:]
        
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
            print(f"p={p}: OK")
        else:
            print(f"p={p}: Плохо, получил {x}")
            
            
if __name__ == "__main__":
    p = 16
    a_11 = 3 + 10 ** (-p)
    b_1 = -16 + 10 ** (-p)
    A, b = get_A_b(a_11, b_1)

    solver = LuSolverWithPermute(A, np.float64, permute=True)
    x = solver.solve(b)
    assert np.all(np.isclose(x, [1, -7, 4])), f"Не точный ответ"
