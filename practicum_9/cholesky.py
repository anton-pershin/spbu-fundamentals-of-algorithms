import numpy as np
from numpy.typing import ArrayLike


def cholesky(A: ArrayLike) -> ArrayLike:

    A = np.asarray(A, dtype=float)
    n = A.shape[0]
    L = np.zeros_like(A)
    for i in range(n):
        for j in range(i):
            L[i, j] = (A[i, j] - L[i, :j] @ L[j, :j]) / L[j, j]
        L[i, i] = np.sqrt(A[i, i] - L[i, :i] @ L[i, :i])
    return L


if __name__ == "__main__":
    L = np.array(
        [
            [1.0, 0.0, 0.0],
            [4.0, 2.0, 0.0],
            [6.0, 5.0, 3.0],
        ]
    )
    A = L @ L.T
    L = cholesky(A)
    print(L)
