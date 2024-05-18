import numpy as np


def cholesky(A):
    L = np.zeros_like(A)
    for i in range(A.shape[0]):
        for j in range(i+1):
            if i == j:
                summ=np.sum(L[i,:j]**2)
                L[i, j] = np.sqrt(A[i, i] - summ)
            else:
                summ = np.sum(L[i, :j] * L[j, :j])
                L[i, j] = (A[i, j] - summ) / L[j, j]
    return L




if __name__ == "__main__":
    L    = np.array(
        [
            [1.0, 0.0, 0.0],
            [4.0, 2.0, 0.0],
            [6.0, 5.0, 3.0],
        ]
    )
    A = L @ L.T
    print("A:")
    print(A)

    L=cholesky(A)
    print("\nCholesky L:")
