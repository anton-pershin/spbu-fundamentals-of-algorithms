import numpy as np


def cholesky(A):
    n = len(A)
    L = np.zeros((n, n))

    for i in range(n):
        for j in range(i+1):
            summ = 0
            for k in range(j):
                summ += (L[i][k] * L[j][k])
            if i == j:
                L[i][j] = np.sqrt(A[i][i] - summ)
            else:
                L[i][j] = (1.0 / L[j][j] * (A[i][j] - summ))

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
    
