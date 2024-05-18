import numpy as np
import matplotlib.pyplot as plt

from src.common import NDArrayFloat


def qr(A: NDArrayFloat) -> tuple[NDArrayFloat, NDArrayFloat]:
    Q = np.zeros_like(A)
    W = A.copy()
    R = np.zeros_like(A)
    for i in range(A.shape[0]):
        w_j_norm = np.linalg.norm(W[:, i])
        Q[:, i] = W[:, i] / w_j_norm
        for j in range(i):
            R[j, i] = A[:, i] @ Q[:, j]
        a_j_norm = np.linalg.norm(A[:, i])
        R[i, i] = np.sqrt(a_j_norm**2 - np.sum(R[:i, i]**2))
        for k in range(i + 1, A.shape[0]):
            prod = W[:, k] @ Q[:, i]
            W[:, k] = W[:, k] - prod * Q[:, i]

    return Q, R


def get_eigenvalues_via_qr(A: NDArrayFloat, n_iters: int) -> NDArrayFloat:
    A_k = A
    for k in range(n_iters):
        Q, R = qr(A_k)
        A_k = R @ Q 
    return np.diag(A_k)


def householder_tridiagonalization_by_alicepro(A: NDArrayFloat) -> NDArrayFloat:
    B = np.zeros_like(A)
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            if i == j:
                B[i, j] = A[i, j]
            elif j == i + 1 or j == i - 1:
                B[i, j] = A[i, j] / A[i, i]
            else:
                B[i, j] = 0
    return B


def sign(x):
    return x >= 0


def householder_tridiagonalization(A: NDArrayFloat) -> NDArrayFloat:
    n = A.shape[0]
    A_k = A.copy()
    for k in range(n - 2):
        x_k = np.zeros((n,))
        x_k[k + 1 :] = A_k[k, k + 1 :]
        y_k = np.zeros((n,))
        y_k[k + 1] = -sign(x_k[k + 1]) * np.linalg.norm(x_k)
        u_k = (x_k - y_k) / np.linalg.norm(x_k - y_k)
        H_k = np.eye(n) - 2 * np.outer(u_k, u_k)
        A_k = H_k @ A_k @ H_k
    return A_k


if __name__ == "__main__":
    A = np.array(
        [
            [4.0, 1.0, -1.0, 2.0],
            [1.0, 4.0, 1.0, -1.0],
            [-1.0, 1.0, 4.0, 1.0],
            [2.0, -1.0, 1.0, 1.0],
        ]
    )
    eigvals = get_eigenvalues_via_qr(A, n_iters=20)

    A_tri = householder_tridiagonalization_by_alicepro(A)
    print(A_tri)
    eigvals_tri = get_eigenvalues_via_qr(A_tri, n_iters=20)
    print(eigvals_tri)

    print()

    A_tri = householder_tridiagonalization(A)
    print(A_tri)
    eigvals_tri = get_eigenvalues_via_qr(A_tri, n_iters=20)
    print(eigvals_tri)
