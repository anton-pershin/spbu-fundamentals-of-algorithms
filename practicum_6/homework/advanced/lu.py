from collections import defaultdict
from dataclasses import dataclass
import os
import time
import yaml


import numpy as np
from numpy.typing import NDArray
import scipy.io
import scipy.linalg

from src.linalg import get_scipy_solution

@dataclass
class Performance:
    time: float = 0.0
    relative_error: float = 0.0
def lu(A: NDArray, permute: bool) -> tuple[NDArray, NDArray, NDArray]:

    n = len(A)
    U = np.copy(A)
    L = np.eye(n)
    P = np.eye(n)

    for k in range(n - 1):
        if permute:
            max_index = np.argmax(abs(U[k:, k])) + k
            if max_index != k:
                U[[k, max_index]] = U[[max_index, k]]
                P[[k, max_index]] = P[[max_index, k]]
                if k != 0:
                    L[[k, max_index], :k] = L[[max_index, k], :k]

        for s in range(k + 1, n):
            L[s][k] = U[s][k] / U[k, k]
            U[s] -= U[k] * U[s][k] / U[k, k]

    return L, U, P
def solve(L: NDArray, U: NDArray, P: NDArray, b: NDArray) -> NDArray:

    n = U.shape[0]
    x, y = np.zeros(n), np.zeros(n)
    b_rearranged = P.dot(b)

    for i in range(n):
        y[i] = b_rearranged[i] - L[i, :i].dot(y[:i])

    for i in range(n-1, -1, -1):
        x[i] = (y[i] - U[i, i+1:].dot(x[i+1:])) / U[i, i]

    return x
def run_test_cases(n_runs: int, path_to_homework: str) -> dict[str, Performance]:
    matrix_filenames = []
    performance_by_matrix = defaultdict(Performance)
    with open(os.path.join(path_to_homework, "matrices.yaml"), "r") as f:
        matrix_filenames = yaml.safe_load(f)
    for i, matrix_filename in enumerate(matrix_filenames):
        print(f"Processing matrix {i+1} out of {len(matrix_filenames)}")
        A = (
            scipy.io.mmread(os.path.join(path_to_homework, "matrices", matrix_filename))
            .todense()
            .A
        )
        b = np.ones((A.shape[0],))
        perf = performance_by_matrix[matrix_filename]
        for j in range(n_runs):
            t1 = time.time()
            L, U, P = lu(A, permute=True)
            t2 = time.time()
            perf.time += t2 - t1
            if j == 0:  # first run => compute solution
                x = solve(L, U, P, b)
                x_exact = get_scipy_solution(A, b)
                perf.relative_error = np.linalg.norm(x - x_exact) / np.linalg.norm(
                    x_exact
                )
    return performance_by_matrix


if __name__ == "__main__":
    n_runs = 10
    path_to_homework = os.path.join("practicum_6", "homework", "advanced")
    performance_by_matrix = run_test_cases(
        n_runs=n_runs, path_to_homework=path_to_homework
    )

    print("\nResult summary:")
    for filename, perf in performance_by_matrix.items():
        print(
            f"Matrix: {filename}. "
            f"Average time: {perf.time / n_runs:.2e} seconds. "
            f"Relative error: {perf.relative_error:.2e}"
        )
