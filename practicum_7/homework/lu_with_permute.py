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
        n = len(b)
        y = np.zeros(n, dtype=self.dtype)
        x = np.zeros(n, dtype=self.dtype)
        
        # Переставляем правую сторону согласно матрице перестановок
        b_perm = np.dot(self.P, b)
        
        # Прямой ход — вычисление вектора y из Ly=P*b
        for i in range(n):
            s = 0
            for j in range(i):
                s += self.L[i, j]*y[j] 
            y[i] = (b_perm[i] - s)/self.L[i,i]
        
        # Обратный ход — находим x из Ux=y
        for i in reversed(range(n)):
            s = 0
            for j in range(i+1,n):
                s += self.U[i,j]*x[j]
            x[i] = (y[i]-s)/self.U[i,i]
            
        return x

    def _decompose(self, permute: bool) -> tuple[NDArrayFloat, NDArrayFloat, NDArrayFloat]:
        n = len(self.A)
        L = np.eye(n, dtype=self.dtype)
        U = self.A.copy()
        P = np.eye(n, dtype=int)
        
        for i in range(n):
            if permute:
                # Поиск главного элемента в текущем столбце
                pivot_index = np.argmax(np.abs(U[i:, i])) + i

                # Обмен строк, если необходимо
                if pivot_index != i:
                    U[[i, pivot_index]] = U[[pivot_index, i]]
                    P[[i, pivot_index]] = P[[pivot_index, i]]

            for j in range(i + 1, n):
                factor = U[j, i] / U[i, i]
                L[j, i] = factor
                U[j, :] -= factor * U[i, :] 

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

