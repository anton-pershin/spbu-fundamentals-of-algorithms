from collections import namedtuple
import numpy as np
import matplotlib.pyplot as plt

from numpy.typing import NDArray
ProblemCase = namedtuple("ProblemCase", "input, output")
NDArrayInt = NDArray[np.int_]
NDArrayFloat = NDArray[np.float_]

def custom_inverse_power_method(A: NDArrayFloat, n_iters: int) -> NDArrayFloat:
    A = np.linalg.inv(A)
    min_eigenvalue_history = np.zeros((n_iters,))
    u_k = np.random.random(A.shape[0])
    u_kk = np.zeros_like(u_k)
    for k in range(n_iters):
        pre_u_kk = A @ u_k
        A_u_k_norm = np.linalg.norm(pre_u_kk)
        u_kk = pre_u_kk / A_u_k_norm
        max_eigenvalue = A_u_k_norm * u_kk[0] / u_k[0]
        u_k = u_kk
        min_eigenvalue_history[k] = (1/max_eigenvalue)
    return min_eigenvalue_history

if __name__ == "__main__":
    A = np.array(
        [
        [4.0, 1.0, -1.0, 2.0],
        [1.0, 4.0, 1.0, -1.0],
        [-1.0, 1.0, 4.0, 1.0],
        [2.0, -1.0, 1.0, 1.0],
        ]
    )
    eigvals = custom_inverse_power_method(A, n_iters=10)
    print(eigvals)
