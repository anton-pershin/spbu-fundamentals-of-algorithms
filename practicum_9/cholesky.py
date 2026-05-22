import numpy as np
from numpy.typing import ArrayLike


def cholesky(A: ArrayLike) -> ArrayLike:
    n = A.shape[0]

    L = np.zeros((n,n), dtype=float)

    for i in range(n):
        for j in range(i+1):
            if (i == j):
                sumDiag = np.sum(L[i,:i]**2)
                val = A[i,i] - sumDiag
                if val <= 0:
                    raise ValueError("Must Be positive-definite")
                L[i,i] = np.sqrt(val)
            else:
                sumOffDiag = np.sum(L[i,:j] * L[j,:j])
                L[i,j] = (A[i,j] - sumOffDiag) / L[j,j]
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
