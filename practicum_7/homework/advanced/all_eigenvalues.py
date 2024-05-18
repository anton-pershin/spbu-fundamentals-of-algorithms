from collections import defaultdict
from dataclasses import dataclass
import os
import yaml
import time


import numpy as np
import scipy.io
import scipy.linalg

from src.linalg import get_numpy_eigenvalues
from numpy.typing import NDArray

NDArrayFloat = NDArray[np.float_]

@dataclass
class Performance:
    time: float = 0.0
    relative_error: float = 0.0

def sign(x):
    return 1 if x > 0 else -1

def householder_qr(A: NDArrayFloat) -> tuple[NDArrayFloat, NDArrayFloat]:
    n = A.shape[0]
    Q = np.eye(n)

    for i in range(n):
        v_i:NDArrayFloat = A[i:, i].copy()
        v_i[0] += sign(v_i[0]) * np.linalg.norm(v_i)
        v_i = v_i.astype(float)
        v_i /= np.linalg.norm(v_i)

        H = np.eye(n)
        H[i:, i:] -= 2.0 * np.matrix(v_i).T @ np.matrix(v_i)

        A = np.dot(H, A)   #втреуг
        Q = np.dot(Q, H.T)   

    return Q, A

def wilkinson_shift(A):
    n = A.shape[0]
    a = A[n - 2, n - 2]
    b = A[n - 2, n - 1]
    c = A[n - 1, n - 1]
    if abs(a - c) < abs(b):
        shift = c
    else:
        shift = a
    return shift

def get_all_eigenvalues(A: NDArrayFloat) -> NDArrayFloat:
    n = A.shape[0]
    E = np.eye(n)
    n_iters = 1
    for _ in range(n_iters):
        shift = wilkinson_shift(A)
        Q, R = householder_qr(A - shift * E)
        A = R @ Q + shift * E      #diag
        ans_proximity = np.sum(np.abs(A - np.diag(np.diag(A))))
        if ans_proximity < 1e3:
            break
    return np.diag(A)


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
        eigvals1 = eigvals.copy()
        eigvals1.sort()
        perf.relative_error = np.median(
            np.abs(eigvals_exact - eigvals1) / np.abs(eigvals_exact)
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
