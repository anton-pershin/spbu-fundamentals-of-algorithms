import numpy as np
import matplotlib.pyplot as plt

from src.common import NDArrayFloat


def power_method(A: NDArrayFloat, n_iters: int):
    x = np.random.random(A.shape[0])
    for _ in range(n_iters):
        x = A @ x
        x = x / np.linalg.norm(x)

    eigenval_max = np.dot(x.T, A @ x) / np.dot(x.T, x)
    return eigenval_max, x


def inverse_power_method(A: NDArrayFloat, n_iters: int) -> NDArrayFloat:
    A_inv = np.linalg.inv(A)
    return power_method(A_inv, n_iters)


if __name__ == "__main__":
    A = np.array(
        [
            [4.0, 1.0, -1.0, 2.0],
            [1.0, 4.0, 1.0, -1.0],
            [-1.0, 1.0, 4.0, 1.0],
            [2.0, -1.0, 1.0, 1.0],
        ]
    )
    eigvals = inverse_power_method(A, n_iters=10)