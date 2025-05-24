from abc import ABC, abstractmethod

import numpy as np
from numpy.typing import DTypeLike
from numpy.linalg import linalg
#from practicum_7.lu import LinearSystemSolver
from src.common import NDArrayFloat

class LinearSystemSolver(ABC):
    def __init__(self, A: NDArrayFloat, dtype: DTypeLike) -> None:
        self.A = A.astype(dtype)
        self.dtype = dtype

    @abstractmethod
    def solve(b: NDArrayFloat) -> NDArrayFloat:
        pass


class LuSolverWithPermute(LinearSystemSolver):
    def __init__(self, A: NDArrayFloat, dtype: DTypeLike, permute: bool) -> None:
        super().__init__(A, dtype)
        self.L, self.U, self.P = self._decompose(permute)

    def solve(self, b: NDArrayFloat) -> NDArrayFloat:

        per_b = self.P @ b

        n = self.L.shape[0]
        y = np.zeros_like(per_b, dtype=self.L.dtype)
        for i in range(n):
            y[i] = per_b[i] - np.dot(self.L[i, :i], y[:i])

        x = np.zeros_like(y, dtype=self.U.dtype)
        for i in range(n - 1, -1, -1):
            x[i] = (y[i] - np.dot(self.U[i, i + 1:], x[i + 1:])) / self.U[i, i]

        return x

    def _decompose(self, permute: bool) -> tuple[NDArrayFloat, NDArrayFloat, NDArrayFloat]:

        n = self.A.shape[0]
        U = self.A.copy()
        P = np.eye(n, dtype=self.A.dtype)
        L = np.eye(n, dtype=self.A.dtype)

        for k in range(n-1):
            if permute:
                main_row = np.argmax(np.abs(U[k:, k])) + k #к т.к. срез массив k: уменьшается с каждым шагом

                if main_row != k:
                    U[[k, main_row], :] = U[[main_row, k], :]
                    L[[k, main_row], :k] = L[[main_row, k], :k]
                    P[[k, main_row]] = P[[main_row, k]]
            if U[k, k] == 0:
                raise ValueError("Zero diagonal element")

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
    print(x)
    assert np.all(np.isclose(x, [1, -7, 4])), f"The anwser {x} is not accurate enough"

