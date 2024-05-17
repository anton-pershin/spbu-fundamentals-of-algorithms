import numpy as np
import math as math


def cholesky(A):
    n = A.shape[0]
    L = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1):
            sum = 0
            for k in range(j + 1):
                sum += L[i][k] * L[j][k]
            if i == j:
                L[i][i] = math.sqrt(A[i][i] - sum)
            else:
                L[i][j] = (1.0 / L[j][j]) * (A[i][j] - sum)

    return L


if __name__ == "__main__":
    float_formatter = "{:.1f}".format
    np.set_printoptions(formatter={'float_kind': float_formatter})
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