from collections import defaultdict
from dataclasses import dataclass
import os
import yaml
import time


import numpy as np
import scipy.io
import scipy.linalg

from src.common import NDArrayFloat
from src.linalg import get_numpy_eigenvalues


@dataclass
class Performance:
    time: float = 0.0
    relative_error: float = 0.0

def qr(A: NDArrayFloat) -> tuple[NDArrayFloat, NDArrayFloat]:
    n = A.shape[0]
    W = np.copy(A)
    Q = np.zeros_like(A)
    R = np.zeros_like(A)
    
    for i in range(n):
        v = W[:, i]
        R[i, i] = np.linalg.norm(v)
        Q[:, i] = v / R[i, i]
        for j in range(i+1, n):
            R[j, i] = Q[:, j] @ W[:, i]
            v = v - R[j, i] * Q[:, j]

    return Q, R

def hessenberg_reduction(A: NDArrayFloat) -> NDArrayFloat:
    n = A.shape[0]
    
    hess = A.copy()
    for k in range(n - 1):
        x = hess[k+1:, k].copy()
    
        norm = np.linalg.norm(x) * sign(x[0])
        
        if (norm == 0):
            continue
        
        h = x[0] + norm
        gamma = h / norm
        
        u = np.zeros_like(x)
        u[0] = 1
        u[1:] = x[1:] / h
        
        v = gamma * u
        
        hess[k+1:, k:] = hess[k+1:, k:] - np.outer(v, u @ hess[k+1:, k:])
        hess[:, k+1:] = hess[:, k+1:] - np.outer(hess[:, k+1:] @ v, u)

    return hess

def sign(x):
    return 1 if x > 0 else -1

def get_all_eigenvalues(A: NDArrayFloat) -> NDArrayFloat:
    A_hess = hessenberg_reduction(A)
    
    n_iters = 1
    for _ in range(n_iters):
        Q, R = qr(A_hess)
        W = R @ Q
    eigen = np.diag(W)

    eig = np.zeros(A.shape[0], dtype=complex)
    for x in range(len(eigen)):
        eig[x] = np.complex64(eigen[x])
    return eig

def run_test_cases(
    path_to_homework: str, path_to_matrices: str
) -> dict[str, Performance]:
    matrix_filenames = []
    performance_by_matrix = defaultdict(Performance)
    with open(os.path.join(path_to_homework, "matrices.yaml"), "r") as f:
        matrix_filenames = yaml.safe_load(f)
    for i, matrix_filename in enumerate(matrix_filenames):
        print(f"Processing matrix {i+1} out of {len(matrix_filenames)}")
        A = scipy.io.mmread(os.path.join(path_to_matrices, matrix_filename)).todense().A

        perf = performance_by_matrix[matrix_filename]
        t1 = time.time()
        eigvals = get_all_eigenvalues(A)
        t2 = time.time()
        perf.time += t2 - t1
        eigvals_exact = get_numpy_eigenvalues(A)
        eigvals_exact.sort()
        eigvals.sort()
        perf.relative_error = np.median(
            np.abs(eigvals_exact - eigvals) / np.abs(eigvals_exact)
        )
    return performance_by_matrix


if __name__ == "__main__":
    path_to_homework = os.path.join("practicum_7", "homework", "advanced")
    path_to_matrices = os.path.join("practicum_6", "homework", "advanced", "matrices")
    performance_by_matrix = run_test_cases(
        path_to_homework=path_to_homework,
        path_to_matrices=path_to_matrices,
    )

    print("\nResult summary:")
    for filename, perf in performance_by_matrix.items():
        print(
            f"Matrix: {filename}. "
            f"Average time: {perf.time:.2e} seconds. "
            f"Relative error: {perf.relative_error:.2e}"
        )