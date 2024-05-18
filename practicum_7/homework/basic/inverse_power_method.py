import numpy as np
import matplotlib.pyplot as plt

from src.common import NDArrayFloat


def inverse_power_method(A: NDArrayFloat, n_iters: int) -> NDArrayFloat:
    u_k = np.random.rand(A.shape[1])  # Создаем рандомный вектор
    u_k = u_k / np.linalg.norm(u_k)

    history = []  # Список для сохранения истории минимальных собственных чисел

    for _ in range(n_iters):  # Следующий вектор
        pre_u_kk = np.linalg.solve(A, u_k)
        A_u_k_norm = np.linalg.norm(pre_u_kk)
        u_k = pre_u_kk / A_u_k_norm

        # Вычисляем приближение к наименьшему по модулю собственному числу матрицы A
        eigenvalue = np.linalg.norm(np.dot(A, u_k)) / np.linalg.norm(u_k)
        history.append(eigenvalue)

    return history


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
