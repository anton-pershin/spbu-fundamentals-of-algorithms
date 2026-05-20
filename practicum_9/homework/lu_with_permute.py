from abc import ABC, abstractmethod

from scipy.io import mmread
import numpy as np
from numpy.typing import DTypeLike

from practicum_9.lu import LinearSystemSolver
from src.common import NDArrayFloat


class LuSolverWithPermute(LinearSystemSolver):
    def __init__(self, A: NDArrayFloat, dtype: DTypeLike, permute: bool) -> None:
        super().__init__(A, dtype)
        self.L, self.U, self.P = self._decompose(permute)

    def solve(self, b: NDArrayFloat) -> NDArrayFloat:
        n = b.shape[0]
        b_permutate = self.P @ b
        y = np.zeros(n, dtype=self.dtype)
        x = np.zeros(n, dtype=self.dtype)

        for i in range(n):
            y[i] = b_permutate[i] - self.L[i, :i] @ y[:i]

        for i in range(n-1, -1, -1):
            x[i] = (y[i] - self.U[i,i+1:] @ x[i+1:])/self.U[i,i]

        return x


    def _decompose(self, permute: bool) -> tuple[NDArrayFloat, NDArrayFloat, NDArrayFloat]:

        n = self.A.shape[0]
        U = self.A.copy()
        L = np.eye(n, dtype=self.dtype)
        P = np.eye(n, dtype=self.dtype)

        for i in range(n - 1):
            if permute:
                indx_max = i + np.argmax(np.abs(U[i:, i]))
                if indx_max != i:
                    U[[i, indx_max]] = U[[indx_max, i]]
                    P[[i, indx_max]] = P[[indx_max, i]]
                    L[[i, indx_max], :i] = L[[indx_max, i], :i]
            L[(i + 1):, i] = U[(i + 1):, i] / U[i][i]
            U[(i + 1):, i:] -= np.outer(L[(i + 1):, i], U[i, i:])
        return L, U, P


def get_A_b(a_11: float, b_1: float) -> tuple[NDArrayFloat, NDArrayFloat]:
    A = np.array([[a_11, 1.0, -3.0], [6.0, 2.0, 5.0], [1.0, 4.0, -3.0]])
    b = np.array([b_1, 12.0, -39.0])
    return A, b


def test_with_matrix_market(filename):

    A_sparse = mmread(filename)
    A = A_sparse.toarray()

    n = A.shape[0]

    x_true = np.ones(n)

    b = A @ x_true

    solver = LuSolverWithPermute(A, np.float64, permute=True)
    x_computed = solver.solve(b)

    error = np.linalg.norm(x_computed - x_true) / np.linalg.norm(x_true)
    print(f"Относительная ошибка: {error:.2e}")

    residual = np.linalg.norm(A @ x_computed - b) / np.linalg.norm(b)
    print(f"Относительная невязка: {residual:.2e}")

    return error, residual


error1, residual1 = test_with_matrix_market('mcca.mtx')
error1, residual1 = test_with_matrix_market('mcfe.mtx')


if __name__ == "__main__":
    p = 16  # modify from 7 to 16 to check instability
    a_11 = 3 + 10 ** (-p)  # add/remove 10**(-p) to check instability
    b_1 = -16 + 10 ** (-p)  # add/remove 10**(-p) to check instability
    A, b = get_A_b(a_11, b_1)

    solver = LuSolverWithPermute(A, np.float64, permute=True)
    x = solver.solve(b)
    assert np.all(np.isclose(x, [1, -7, 4])), f"The anwser {x} is not accurate enough"

