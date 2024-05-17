from collections import defaultdict
from dataclasses import dataclass
import os
import yaml
import time

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
    L = np.eye(n)
    U = np.copy(A)
    P = np.eye(n)

    for column in range(n-1):
        n = len(A)
        U = np.copy(A)
        L = np.eye(n)
        P = np.eye(n)
        for k in range(n - 1):
            if permute == True:
                max_el = np.argmax(abs(U[k:, k])) + k #Find abs max element, it will be a pivot
                if max_el != k: #If it's not on main diagonal, then swap lines
                    P[[k, max_el]] = P[[max_el, k]]
                    U[[k, max_el]] = U[[max_el, k]]
                    if k != 0:
                        L[[k, max_el], :k] = L[[max_el, k], :k]
            
            for i in range(k + 1, n):
                m = U[i, k] / U[k, k]
                L[i, k] = m
                U[i] -= (U[k] * m)
        return L, U, P
       


def solve(L: NDArray, U: NDArray, P: NDArray, b: NDArray) -> NDArray:
    n = len(b)
    y = np.zeros(n)
    x = np.zeros(n)

    rearranged_b = P.dot(b) # Swaped columns in b, using P
    
    # Firstly, solve Ly = Pb, where y = Ux    
    for i in range(n):
        y[i] = rearranged_b[i] - np.dot(L[i, :i], y[:i])
    # Secondly, solve y = Ux and find x
    for i in range(n-1, -1, -1):
        x[i] = (y[i] - np.dot(U[i, i+1:], x[i+1:])) / U[i, i]
        
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
    n_runs = 1
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
        
