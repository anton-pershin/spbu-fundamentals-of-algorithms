from collections import defaultdict
from dataclasses import dataclass
import os
import yaml

import time as tm

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
    n = A.shape[0]
    P = np.eye(n)
    U = np.copy(A)
    L = np.eye(n)
    for j in range(n):
        if permute:
            max_index = np.argmax(np.abs(U[j:, j])) + j
            U[[j, max_index]] = U[[max_index, j]]
            P[[j, max_index]] = P[[max_index, j]]
        for i in range(j + 1, n):
            L[i, j] = U[i, j] / U[j, j] ### lu - разложение
            U[i, j:] -= L[i, j] * U[j, j:]

    return L, U, P


def solve(L: NDArray, U: NDArray, P: NDArray, b: NDArray) -> NDArray:
    n = L.shape[0]
    y = P @ b 
    x = np.zeros_like(y)
    for i in range(n):
        x[i] = (y[i] - L[i, :i] @ x[:i]) / L[i, i]
    for j in range(n-1, -1, -1):
        x[j] = (x[j] - U[j, j + 1:] @ x[j + 1:]) / U[j, j]
    return x


def run_test_cases(n_runs: int, path_to_homework: str) -> dict[str, Performance]:
    matrix_filenames = []
    performance_by_matrix = defaultdict(Performance)
    with open(os.path.join(path_to_homework, "matrices.yaml"), "r") as f:
        matrix_filenames = yaml.safe_load(f)
    for i, matrix_filename in enumerate(matrix_filenames):
        print(f"Processing matrix {i + 1} out of {len(matrix_filenames)}")
        A = (
            scipy.io.mmread(os.path.join(path_to_homework, "matrices", matrix_filename))
            .todense()
            .A
        )
        b = np.ones((A.shape[0],))
        perf = performance_by_matrix[matrix_filename]
        for j in range(n_runs):
            t1 = tm.time()
            L, U, P = lu(A, permute=True)
            t2 = tm.time()
            perf.time += t2 - t1
            if j == 0:  # first run => compute solution
                x = solve(L, U, P, b)
                x_exact = get_scipy_solution(A, b)
                perf.relative_error = np.linalg.norm(x - x_exact) / np.linalg.norm(
                    x_exact
                )
    return performance_by_matrix


if __name__ == "__main__":
    n_runs = 1
    path_to_homework = ""
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
