from collections import defaultdict
from dataclasses import dataclass
import os
import yaml
import time as tm


import numpy as np
from numpy.typing import NDArray

import scipy.io
import scipy.linalg

from src.linalg import get_numpy_eigenvalues

NDArrayFloat = NDArray[np.float_]
@dataclass
class Performance:
    time: float = 0.0
    relative_error: float = 0.0


def get_all_eigenvalues(A: NDArrayFloat) -> NDArrayFloat:
    n = A.shape[0]
    A_k = np.copy(A)
    t = 1e-10
    for _ in range(n):
        Q, R = modified_gram_schmidt(A_k)
        A_k = np.dot(R, Q)
        off_diag = np.sqrt(np.sum(np.tril(A_k, -1) ** 2))
        if off_diag < t:
            break
    eigenvalues = np.diag(A_k)
    return eigenvalues

def modified_gram_schmidt(A):
    m, n = A.shape
    Q = np.zeros((m, n))
    R = np.zeros((n, n))

    for k in range(n):
        v = A[:, k]
        for j in range(k):
            R[j, k] = np.dot(Q[:, j], v)
            v -= R[j, k] * Q[:, j]
        Q[:, k] = v
        R[k, k] = np.linalg.norm(Q[:, k])
        Q[:, k] = Q[:, k] / R[k, k]

    return Q, R

def run_test_cases(
    path_to_homework: str, path_to_matrices: str
) -> dict[str, Performance]:
    matrix_filenames = []
    performance_by_matrix = defaultdict(Performance)
    with open(os.path.join("matrices.yaml"), "r") as f:
        matrix_filenames = yaml.safe_load(f)
    for i, matrix_filename in enumerate(matrix_filenames):
        print(f"Processing matrix {i+1} out of {len(matrix_filenames)}")
        A = scipy.io.mmread(os.path.join(path_to_matrices, matrix_filename)).todense().A
        perf = performance_by_matrix[matrix_filename]
        t1 = tm.time()
        eigvals = get_all_eigenvalues(A)
        t2 = tm.time()
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
