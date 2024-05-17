import numpy as np
import matplotlib.pyplot as plt

from src.common import NDArrayFloat


def inverse_power_method(A: NDArrayFloat, n_iters: int) -> NDArrayFloat:
    n = A.shape[0]
    x = np.random.rand(n)
    x /= np.linalg.norm(x)

    for _ in range(n_iters):
        b_k = np.linalg.solve(A, x)
        b_k_norm = np.linalg.norm(b_k)
        x = b_k / b_k_norm
        eigval = np.dot(x, b_k)

    return eigval


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
    print("Estimated Eigenvalue:", eigvals)
