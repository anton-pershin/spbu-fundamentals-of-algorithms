import numpy as np
import matplotlib.pyplot as plt


def inverse_power_method(A, n_iters: int):
    x = np.random.rand(A.shape[0])

    for _ in range(n_iters):
        y = np.dot(A, x)
        x = y / np.linalg.norm(y)

    eigenvalue = np.dot(x, np.dot(A, x))

    return eigenvalue

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
