import numpy as np
from numpy.typing import NDArray
import networkx as nx
from random import random
from math import e, log

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


def tweak(colors, n_max_colors):
    new_colors = colors.copy()
    n_nodes = len(new_colors)
    random_i = np.random.randint(low=0, high=n_nodes)
    random_color = np.random.randint(low=0, high=n_max_colors)
    new_colors[random_i] = random_color
    return new_colors


def solve_via_simulated_annealing(
        G: nx.Graph, n_max_colors: int, initial_colors: NDArrayInt, n_iters: int
):
    loss_history = np.zeros((n_iters,), dtype=np.int_)
    temperature = n_iters
    cur_colors = initial_colors.copy()
    next_colors = initial_colors.copy()
    n_conflicts_best = number_of_conflicts(G, cur_colors)

    for i in range(n_iters):
        loss_history[i] = number_of_conflicts(G, cur_colors)
        next_colors = tweak(cur_colors.copy(), n_max_colors)
        delta_conflicts = n_conflicts_best - number_of_conflicts(G, next_colors)
        eps = random()

        if (delta_conflicts > 0) or (eps < e ** (delta_conflicts / temperature)):
            cur_colors = next_colors
            n_conflicts_best = number_of_conflicts(G, cur_colors)

        if temperature / log(i + 2) != 0:
            temperature /= log(i + 2)

    return loss_history


if __name__ == "__main__":
    seed = 42
    np.random.seed(seed)
    G = nx.erdos_renyi_graph(n=100, p=0.05, seed=seed)

    n_max_iters = 500
    n_max_colors = 3
    initial_colors = np.random.randint(low=0, high=n_max_colors - 1, size=len(G.nodes))

    loss_history = solve_via_simulated_annealing(
        G, n_max_colors, initial_colors, n_max_iters
    )
