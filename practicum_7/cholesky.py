import numpy as np
from numpy.typing import ArrayLike


def cholesky(A: ArrayLike) -> ArrayLike:

    ##########################
    ### PUT YOUR CODE HERE ###
    ##########################

    pass


if __name__ == "__main__":
    L = np.array(
        [
            [1.0, 0.0, 0.0],
            [4.0, 2.0, 0.0],
            [6.0, 5.0, 3.0],
        ]
    )
    A = L @ L.T
    L = cholesky(A)
    print(L)
