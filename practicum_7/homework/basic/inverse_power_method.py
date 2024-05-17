import numpy as np
import matplotlib.pyplot as plt

from src.common import NDArrayFloat


def inverse_power_method(A: NDArrayFloat, n_iters: int) -> NDArrayFloat:
    n = A.shape[0]
    Q = np.random.randn(n, n)
    Q, _ = np.linalg.qr(Q)
    for _ in range(n_iters):
        Q = np.linalg.solve(A, Q)
        Q, _ = np.linalg.qr(Q)
    return np.diag(Q.T @ A @ Q)

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
    print(eigvals)
