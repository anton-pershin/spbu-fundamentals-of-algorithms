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

        ##########################
        ### PUT YOUR CODE HERE ###
        ##########################

        pass

    def _decompose(self) -> tuple[NDArrayFloat, NDArrayFloat]:

        ##########################
        ### PUT YOUR CODE HERE ###
        ##########################

        pass


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

