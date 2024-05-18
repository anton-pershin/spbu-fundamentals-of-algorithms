import os

import numpy as np
import scipy.io
import matplotlib.pyplot as plt

from src.common import NDArrayFloat
from src.linalg import get_scipy_solution


def fixed_point_iteration(
    T: NDArrayFloat, c: NDArrayFloat, n_iters: int
) -> NDArrayFloat:

    ##########################
    ### PUT YOUR CODE HERE ###
    ##########################

    pass


def jacobi_method(A: NDArrayFloat, b: NDArrayFloat, n_iters: int) -> NDArrayFloat:

    ##########################
    ### PUT YOUR CODE HERE ###
    ##########################

    pass


def gauss_seidel_method(A: NDArrayFloat, b: NDArrayFloat, n_iters: int) -> NDArrayFloat:

    ##########################
    ### PUT YOUR CODE HERE ###
    ##########################

    pass


def relaxation_method(
    A: NDArrayFloat, b: NDArrayFloat, omega: float, n_iters: int
) -> NDArrayFloat:

    ##########################
    ### PUT YOUR CODE HERE ###
    ##########################

    pass


def relative_error(x_true, x_approx):
    return np.linalg.norm(x_true - x_approx, axis=1) / np.linalg.norm(x_true)


def make_axis_pretty(ax):
    ax.grid()
    ax.legend(fontsize=12)
    ax.set_xlabel("Iteration", fontsize=12)
    ax.set_ylabel(r"$||x - \tilde{x}|| / ||x||$", fontsize=12)


if __name__ == "__main__":
    np.random.seed(42)

    # You can also experiment with the following matrices:
    # nos5.mtx.gz (pos.def., K = O(10^4))
    # bcsstk14.mtx.gz (pos.def., K = O(10^10))

    path_to_matrix = os.path.join(
        "practicum_6", "homework", "advanced", "matrices", "orsirr_1.mtx.gz"
    )
    A = scipy.io.mmread(path_to_matrix).todense().A
    b = np.ones((A.shape[0],))
    exact_solution = get_scipy_solution(A, b)
    n_iters = 1000

    # Convergence speed for the Jacobi method

    fig, ax = plt.subplots(1, 1, figsize=(10, 5))
    solution_history = jacobi_method(A, b, n_iters=n_iters)
    ax.semilogy(
        range(n_iters),
        relative_error(x_true=exact_solution, x_approx=solution_history),
        "o--",
    )
    make_axis_pretty(ax)
    plt.show()

    # Convergence speed for the Gauss-Seidel method

    fig, ax = plt.subplots(1, 1, figsize=(10, 5))
    solution_history = gauss_seidel_method(A, b, n_iters=n_iters)
    ax.semilogy(
        range(n_iters),
        relative_error(x_true=exact_solution, x_approx=solution_history),
        "o--",
    )
    make_axis_pretty(ax)
    plt.show()

    # Convergence speed for the relaxation method

    fig, ax = plt.subplots(1, 1, figsize=(10, 5))
    for omega in np.arange(1.0, 2.01, 0.1):
        solution_history = relaxation_method(A, b, omega=omega, n_iters=n_iters)
        ax.semilogy(
            range(n_iters),
            relative_error(x_true=exact_solution, x_approx=solution_history),
            "o--",
            label=r"$\omega = " + f"{omega:.1f}" + r"$",
        )
    make_axis_pretty(ax)
    plt.show()
