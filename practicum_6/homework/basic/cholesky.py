import numpy as np


def cholesky(A):
    n = len(A)
    L = np.zeros_like(A)
    
    for i in range(n):
        for j in range(i+1):
            if i == j:
               L[i][j] = np.sqrt(A[i][i] - sum(L[i][k]**2 for k in range(j)))
            else:
                L[i][j] = (1 / L[j][j] * (A[i][j] - sum(L[i][k] * L[j][k] for k in range(j))))
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
