import numpy as np
from numpy.typing import NDArray
import networkx as nx
import random

from src.plotting import plot_graph, plot_loss_history


NDArrayInt = NDArray[np.int_]


def number_of_conflicts(G, colors):
    set_colors(G, colors)
    n = 0
    for n_in, n_out in G.edges:
        if G.nodes[n_in]["color"] == G.nodes[n_out]["color"]:
            n += 1
    return n


def set_colors(G, colors):
    for n, color in zip(G.nodes, colors):
        G.nodes[n]["color"] = color


def solve_via_simulated_annealing(
    G: nx.Graph, n_max_colors: int, initial_colors: NDArrayInt, n_iters: int
):
    loss_history = np.zeros((n_iters,), dtype=np.int_)


    def tweak(current_point):
        new_point = current_point.copy()
        node = np.random.choice(list(G.nodes))
        color = np.random.choice(list(range(n_max_colors)))
        new_point[node] = color
        return new_point

    def reduction(t):
        return 0.9999 * t

    current_point = initial_colors.copy()
    current_conflict = number_of_conflicts(G, current_point)
    T = 1.0
    n_iter = 0

    while n_iter < n_iters and T > 0.1:
            new_point = tweak(current_point)
            new_conflict = number_of_conflicts(G, new_point)
            conflict = new_conflict - current_conflict

            if conflict < 0 or np.random.random() < np.exp(-conflict / T):
                current_point = new_point
                current_conflict = new_conflict

            T = reduction(T)
            loss_history[n_iter] = current_conflict
            n_iter += 1


    return loss_history


if __name__ == "__main__":
    seed = 42
    np.random.seed(seed)
    G = nx.erdos_renyi_graph(n=100, p=0.05, seed=seed)
    plot_graph(G)

    n_max_iters = 1000
    n_max_colors = 3
    initial_colors = np.random.randint(low=0, high=n_max_colors - 1, size=len(G.nodes))

    loss_history = solve_via_simulated_annealing(
        G, n_max_colors, initial_colors, n_max_iters
    )
    plot_loss_history(loss_history)
