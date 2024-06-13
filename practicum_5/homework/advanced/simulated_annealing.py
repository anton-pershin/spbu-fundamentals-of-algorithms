import numpy as np
from numpy.typing import NDArray
import networkx as nx

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


def decrease_temperature(t, lamda=0.99):
    return t * lamda


def tweak(G: nx.Graph, colors: NDArrayInt, n_max_colors: int):
    new_colors = colors.copy()
    new_colors[np.random.randint(0, len(new_colors))] = np.random.randint(0, n_max_colors)

    return new_colors


def solve_via_simulated_annealing(
    G: nx.Graph, n_max_colors: int, initial_colors: NDArrayInt, n_iters: int, temperature=10
):
    loss_history = np.zeros((n_iters,), dtype=np.int_)

    cur_colors = initial_colors
    next_colors = initial_colors.copy()
    next_colors_best = initial_colors.copy()

    for i in range(n_iters):
        loss_history[i] = number_of_conflicts(G, cur_colors)
        new_colors_best = tweak(G, cur_colors, n_max_colors)
        n_conflicts_best = number_of_conflicts(G, new_colors_best)

        n_tweaks = 10
        for _ in range(n_tweaks):
            next_colors = tweak(G, cur_colors, n_max_colors)
            if n_conflicts_best > number_of_conflicts(G, next_colors):
                next_colors_best = next_colors
                n_conflicts_best = number_of_conflicts(G, next_colors)

        chance = np.power(np.exp(1),
                          (- number_of_conflicts(G, new_colors_best) + (number_of_conflicts(G, cur_colors)) / temperature))

        if number_of_conflicts(G, cur_colors) >= number_of_conflicts(G, new_colors_best):
            cur_colors = next_colors_best
        elif chance < np.random.rand():
            # print(chance)
            cur_colors = new_colors_best

        temperature = decrease_temperature(temperature)

    return loss_history


if __name__ == "__main__":
    seed = 42
    np.random.seed(seed)
    G = nx.erdos_renyi_graph(n=100, p=0.05, seed=seed)
    plot_graph(G)

    n_max_iters = 500
    n_max_colors = 3
    temperature = 10
    initial_colors = np.random.randint(low=0, high=n_max_colors - 1, size=len(G.nodes))

    loss_history = solve_via_simulated_annealing(
        G, n_max_colors, initial_colors, n_max_iters
    )
    plot_loss_history(loss_history)
