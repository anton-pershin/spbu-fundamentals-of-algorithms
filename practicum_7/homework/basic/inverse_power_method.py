import numpy as np
import matplotlib.pyplot as plt

from numpy.typing import NDArray

NDArrayFloat = NDArray[np.float_]


def inverse_power_method(A: NDArrayFloat, n_iters: int) -> NDArrayFloat:

    x = np.random.random(A.shape[0])
    x1 = np.zeros_like(x)
    for i in range(n_iters):
        x1 = np.linalg.solve(A, x)
        x1 /=  np.linalg.norm(x1)
        x = x1
    eigvals = np.dot(x, np.dot(A, x))
    return eigvals

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
