import numpy as np
import matplotlib.pyplot as plt

from src.common import NDArrayFloat


def inverse_power_method(A: NDArrayFloat, n_iters: int) -> NDArrayFloat:
    min_eig = np.random.random(A.shape[0])
    min_eig_pr = np.zeros_like(min_eig)
    for i in range(n_iters):
        min_eig_pr = np.linalg.inv(A) @ min_eig
        min_eig_pr /= np.linalg.norm(min_eig_pr)
        min_eig = min_eig_pr
    eigval = np.dot(min_eig, np.dot(A, min_eig))
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
    eigvals = inverse_power_method(A, n_iters=4)
    print(eigvals)