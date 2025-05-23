from abc import ABC, abstractmethod

import numpy as np
from numpy.typing import DTypeLike

from src.common import NDArrayFloat


class LinearSystemSolver(ABC):
    def __init__(self, A: NDArrayFloat, dtype: DTypeLike) -> None:
        self.A = A.astype(dtype)
        self.dtype = dtype

    @abstractmethod
    def solve(b: NDArrayFloat) -> NDArrayFloat:
        pass


class LuSolver(LinearSystemSolver):
    def __init__(self, A: NDArrayFloat, dtype: DTypeLike) -> None:
        super().__init__(A, dtype)
        self.L, self.U = self._decompose()

    def solve(self, b: NDArrayFloat) -> NDArrayFloat:
        n=self.L.shape[0]
        y=np.zeros_like(b,dtype=self.dtype)
        
        for i in range(n):
            y[i]=(b[i]-(self.L[i,:i]@y[:i]))/self.L[i,i]
        x=np.zeros_like(b,dtype=self.dtype)
        
        for i in range(n-1,-1,-1):
            x[i]=(y[i]-(self.U[i,i+1:]@x[i+1:]))/self.U[i,i]
        return x


    def _decompose(self) -> tuple[NDArrayFloat, NDArrayFloat]:
        n=self.A.shape[0]
        U = self.A.copy()
        L=np.eye(n,dtype=self.dtype)

        for k in range(n-1):
            if U[k,k]==0:
                raise ValueError("Zero pivot")
            L[k+1:,k]=U[k+1:,k]/U[k,k]
            U[k+1:,k:]-= np.outer(L[k+1:,k],U[k,k:])
        return L, U


def get_A_b(a_11: float, b_1: float) -> tuple[NDArrayFloat, NDArrayFloat]:
    A = np.array([[a_11, 1.0, -3.0], [6.0, 2.0, 5.0], [1.0, 4.0, -3.0]])
    b = np.array([b_1, 12.0, -39.0])
    return A, b


if __name__ == "__main__":
    p = 7  # modify from 7 to 16 to check instability
    a_11 = 3 + 10 ** (-p)  # add/remove 10**(-p) to check instability
    b_1 = -16 + 10 ** (-p)  # add/remove 10**(-p) to check instability
    A, b = get_A_b(a_11, b_1)

    # Without pivoting
    solver = LuSolver(A, np.float64)
    x = solver.solve(b)
    assert np.all(np.isclose(x, [1, -7, 4])), f"The anwser {x} is not accurate enough"

