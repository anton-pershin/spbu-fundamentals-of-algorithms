import numpy as np
import matplotlib.pyplot as plt
from src.common import NDArrayFloat


def inverse_power_method(A: NDArrayFloat, n_iters: int) -> NDArrayFloat:
    smallest_eigenvalue_history = np.zeros((n_iters,))
    u_k = np.random.random(A.shape[0])
    A_inv = np.linalg.inv(A) #обратная матрица

    for k in range(n_iters):
        pre_u_k = A_inv @ u_k
        u_k_norm = np.linalg.norm(pre_u_k)
        u_k = pre_u_k / u_k_norm
        smallest_eigenvalue = u_k_norm
        smallest_eigenvalue_history[k] = smallest_eigenvalue

    return smallest_eigenvalue_history




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