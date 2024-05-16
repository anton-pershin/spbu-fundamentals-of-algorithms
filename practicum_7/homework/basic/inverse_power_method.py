import numpy as np
import matplotlib.pyplot as plt
from src.common import NDArrayFloat

def inverse_power_method(A: NDArrayFloat, n_iters: int, tol: float = 1e-10) -> NDArrayFloat:
    n = A.shape[0]
    b_k = np.random.rand(n)
    b_k /= np.linalg.norm(b_k)

    for _ in range(n_iters):
        b_k1 = np.linalg.solve(A, b_k)
        b_k1_norm = np.linalg.norm(b_k1)
        b_k = b_k1 / b_k1_norm

        if b_k1_norm < tol:
            break

    eigenvalue = np.dot(b_k.T, np.dot(A, b_k)) / np.dot(b_k.T, b_k)
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
    eigval = inverse_power_method(A, n_iters=10)
    print("Estimated eigenvalue:", eigval)
