import numpy as np


def cholesky(A):
    n = A.shape[0]
    L = np.zeros_like(A)

    for i in range(n):
        for j in range(i + 1):
            if i == j:
                sum_k = np.sum(L[i, :j] ** 2)
                L[i, j] = np.sqrt(A[i, i] - sum_k)
            else:
                sum_k = np.sum(L[i, :j] * L[j, :j])
                L[i, j] = (A[i, j] - sum_k) / L[j, j]

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
