from collections import defaultdict
from dataclasses import dataclass
import os
import yaml
import time

import numpy as np
from numpy.typing import NDArray
import scipy.io
import scipy.linalg
from scipy.linalg import solve_triangular

from src.linalg import get_scipy_solution


@dataclass
class Performance:
    time: float = 0.0
    relative_error: float = 0.0


def find_max_index(A, column_index):
    diagonal_index = column_index
    column = np.abs(A[diagonal_index:, column_index])
    max_index = np.argmax(column)
    return diagonal_index + max_index

def lu(A: NDArray, permute: bool) -> tuple[NDArray, NDArray, NDArray]:
    size_matrix = A.shape[0]

    for x in A:
        row = len(x)
        if row != size_matrix:
            print("Матрица должна быть квадратной")
             
    U = np.copy(A)
    L = np.eye(size_matrix)
    P = np.eye(size_matrix)

    for column_index in range(size_matrix - 1):
        if(permute):
            max_index = find_max_index(U, column_index)

            P[[column_index, max_index]] = P[[max_index, column_index]]
            U[[column_index, max_index]] = U[[max_index, column_index]]

            if column_index > 0:
                L[column_index, :column_index], L[max_index, :column_index] = L[max_index, :column_index].copy(), L[column_index, :column_index].copy()

        diag_elem = U[column_index, column_index]
        if diag_elem == 0:
            print("Диагональный элемент равен нулю")
        
        ratio = U[column_index + 1:, column_index] / diag_elem
        L[column_index + 1:, column_index] = ratio
        U[column_index + 1:] -= U[column_index] * ratio[:, np.newaxis]

    return L, U, P


def solve(L: NDArray, U: NDArray, P: NDArray, b: NDArray) -> NDArray:
    y = solve_triangular(L, P@b, lower=True) #Ly = Pb
    x = solve_triangular(U, y, lower=False) # Ux = y
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
