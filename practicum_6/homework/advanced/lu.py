import os
from collections import defaultdict
from dataclasses import dataclass
import time
import numpy as np
import scipy.io
import scipy.linalg
import yaml
from numpy.typing import NDArray

@dataclass
class Performance:
    time: float = 0.0
    relative_error: float = 0.0


def lu(A: NDArray, permute: bool) -> tuple[NDArray, NDArray, NDArray]:
    n = A.shape[0]
    U = A.copy()
    L = np.eye(n)
    P = np.eye(n)

    for i in range(n):
        if permute:
            max_row = i + np.argmax(np.abs(U[i:n, i]))
            if i != max_row:
                U[[i, max_row]], U[[max_row, i]] = U[[max_row, i]], U[[i, max_row]].copy()
                P[[i, max_row]], P[[max_row, i]] = P[[max_row, i]], P[[i, max_row]].copy()
                if i > 0:
                    L[[i, max_row], :i], L[[max_row, i], :i] = L[[max_row, i], :i], L[[i, max_row], :i].copy()

        for j in range(i + 1, n):
            factor = U[j, i] / U[i, i]
            U[j, i:] -= factor * U[i, i:]
            L[j, i] = factor

    return P, L, U

def solve(L: NDArray, U: NDArray, P: NDArray, b: NDArray) -> NDArray:
    Pb = P @ b   #учет перестановок
    n = L.shape[0]
    y = np.zeros_like(b)  # Lu = Pb
    for i in range(n):
        y[i] = Pb[i] - np.dot(L[i, :i], y[:i])

    x = np.zeros_like(b)  # Ax = b
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - np.dot(U[i, i + 1:], x[i + 1:])) / U[i, i]

    return x

def get_scipy_solution(A, b):
    lu_and_piv = scipy.linalg.lu_factor(A)
    return scipy.linalg.lu_solve(lu_and_piv, b)

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
