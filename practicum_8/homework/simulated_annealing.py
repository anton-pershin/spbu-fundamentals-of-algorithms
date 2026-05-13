import numpy as np
from numpy.typing import NDArray
import networkx as nx

from src.plotting.graphs import plot_graph
from src.plotting.misc import plot_loss_history


NDArrayInt = NDArray[np.int_]


def number_of_conflicts(G: nx.Graph, colors: NDArrayInt) -> int:
    set_colors(G, colors)
    n = 0
    for n_in, n_out in G.edges:
        if G.nodes[n_in]["color"] == G.nodes[n_out]["color"]:
            n += 1
    return n


def set_colors(G: nx.Graph, colors: NDArrayInt) -> None:
    for n, color in zip(G.nodes, colors):
        G.nodes[n]["color"] = color


def tweak(colors: NDArrayInt, n_max_colors: int) -> NDArrayInt:
    new_color = colors.copy()
    node = np.random.randint(0, len(new_color))

    old = new_color[node]
    new = np.random.randint(0, n_max_colors)
    while new == old:
        new = np.random.randint(0, n_max_colors)

    new_color[node] = new
    return new_color


def cooling_schedule(initial_temp: float, i: int) -> float:
    # return initial_temp / np.log(i + 2) # Логарифмическое
    # return initial_temp / (1 + i)  # Коши
    # return initial_temp * (1 - i / n_iters) # Линейное
     return initial_temp * (0.98 ** i) # Экспоненциальное, 0.95-0.99


def solve_via_simulated_annealing(
    G: nx.Graph, n_max_colors: int, initial_colors: NDArrayInt, n_iters: int
) -> NDArrayInt:
    loss_history = np.zeros((n_iters,), dtype=np.int_)

    cur_color = initial_colors.copy() # current color
    cur_cf = number_of_conflicts(G, cur_color) # current number of conflicts

    res = cur_color.copy() # best color variant - result
    min_cf = cur_cf # min number of conflicts

    initial_temp = 100.0 # start temperature

    for i in range(n_iters):
        loss_history[i] = cur_cf

        if cur_cf == 0:
            loss_history[i:] = 0
            break

        temp = cooling_schedule(initial_temp, i) # temperature
        new_color = tweak(cur_color, n_max_colors)
        new_cf = number_of_conflicts(G, new_color) # new number of conflicts

        d = new_cf - cur_cf # difference

        if d <= 0 or np.random.random() < np.exp(-d / temp):
            cur_color = new_color
            cur_cf = new_cf

            if cur_cf < min_cf:
                min_cf = cur_cf
                res = cur_color.copy()

    set_colors(G, res)

    return loss_history


if __name__ == "__main__":
    seed = 42
    np.random.seed(seed)
    G = nx.erdos_renyi_graph(n=100, p=0.05, seed=seed)
    plot_graph(G)

    n_max_iters = 500
    n_max_colors = 3
    initial_colors = np.random.randint(low=0, high=n_max_colors - 1, size=len(G.nodes))

    loss_history = solve_via_simulated_annealing(
        G, n_max_colors, initial_colors, n_max_iters
    )
    plot_loss_history(loss_history)
    print()
