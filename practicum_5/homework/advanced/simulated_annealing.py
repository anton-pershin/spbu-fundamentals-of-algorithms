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


def tweak(G: nx.Graph, colors, n_max_colors):
    new_colors = colors.copy()
    n_nodes = len(new_colors)

    random_i = np.random.randint(low=0, high=n_nodes)
    random_color = np.random.randint(low=0, high=n_max_colors)

    new_colors[random_i] = random_color

    for neighbor in G.neighbors(random_i):
        if new_colors[neighbor] == random_color:
            new_color = (random_color + 1) % n_max_colors
            new_colors[neighbor] = new_color

    return new_colors


def solve_via_simulated_annealing(
        G: nx.Graph, n_max_colors: int, initial_colors: NDArrayInt, n_iters: int
):
    loss_history = np.zeros((n_iters,), dtype=np.int_)

    max_temp = 1000
    coeff = 0.9235
    curr_temp = max_temp
    min_energy = number_of_conflicts(G, initial_colors)
    curr_colors = initial_colors.copy()

    for i in range(n_iters):
        new_colors = tweak(G, curr_colors, n_max_colors)
        energy_diff = number_of_conflicts(G, new_colors) - min_energy

        if energy_diff < 0 or np.exp(-energy_diff / curr_temp) >= np.random.rand():
            curr_colors = new_colors.copy()
            min_energy = number_of_conflicts(G, new_colors)

        curr_temp *= coeff

        loss_history[i] = min_energy

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
    print(f'Количество конфликтов: {loss_history[-1]}')
