from typing import Union, Any

import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray

from src.common import NDArrayInt


def plot_points(points: NDArray, convex_hull: NDArray = None, **kwargs) -> None:
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(points[:, 0], points[:, 1], "o", **kwargs)
    if convex_hull is not None:
        convex_hull = np.concatenate(
            (convex_hull, convex_hull[0, :].reshape(1, -1)), axis=0
        )
        ax.plot(convex_hull[:, 0], convex_hull[:, 1], "-", linewidth=4, zorder=-10)
    ax.grid()
    fig.tight_layout()
    plt.show()


def plot_loss_history(
    loss_history: NDArrayInt, xlabel="# iterations", ylabel="# conflicts"
) -> None:
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    if loss_history.ndim == 1:
        loss_history = loss_history.reshape(1, -1)
    n_restarts, n_iters = loss_history.shape
    for i in range(n_restarts):
        ax.plot(range(n_iters), loss_history[i, :])
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid()
    fig.tight_layout()
    plt.show()
