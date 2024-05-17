import numpy as np
from numpy.typing import NDArray


def lu(A: NDArray, permute: bool) -> tuple[NDArray, NDArray, NDArray]:

    n = A.shape[0]
    L = np.eye(n)
    U = np.copy(A)
    P = np.eye(n)
    U_0 = np.eye(n)

    for k in range(n-1):
        if permute:
            max_index = np.argmax(abs(U[k:, k])) + k
            if max_index != k:
                U[[k, max_index]] = U[[max_index, k]]
                P[[k, max_index]] = P[[max_index, k]]
                if k > 0:
                    L[[k, max_index], :k] = L[[max_index, k], :k]
        for i in range(k + 1, n):
            m = U[i, k] / U[k, k]
            U_0[i, k] = -m
            L[i, k] = m
        U = U_0 @ U
    return L, U, P


def solve(L: NDArray, U: NDArray, P: NDArray, b: NDArray) -> NDArray:
    n = L.shape[0]
    b_permuted = P.dot(b)
     #(Ly = Pb)
    y = np.zeros(n)
    for i in range(n):
        y[i] = b_permuted[i] - L[i, :i].dot(y[:i])

    #(Ux = y)
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        x[i] = (y[i] - U[i, i+1:].dot(x[i+1:])) / U[i, i]

    return x


def get_A_b(a_11: float, b_1: float) -> tuple[NDArray, NDArray]:
    A = np.array([[a_11, 1.0, -3.0], [6.0, 2.0, 5.0], [1.0, 4.0, -3.0]])
    b = np.array([b_1, 12.0, -39.0])
    return A, b


if __name__ == "__main__":
    p = 14  # modify from 7 to 16 to check instability
    a_11 = 3 + 10 ** (-p)  # add/remove 10**(-p) to check instability
    b_1 = -16 + 10 ** (-p)  # add/remove 10**(-p) to check instability
    A, b = get_A_b(a_11, b_1)
    # With pivoting
    L, U, P = lu(A, permute=True)
    x = solve(L, U, P, b)
    assert np.all(np.isclose(x, [1, -7, 4])), f"The anwser {x} is not accurate enough"
    # Without pivoting
    L, U, P = lu(A, permute=False)
    x_ = solve(L, U, P, b)
    assert np.all(np.isclose(x_, [1, -7, 4])), f"The anwser {x_} is not accurate enough"
