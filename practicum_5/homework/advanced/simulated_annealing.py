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


def tweak(colors, n_max_colors, temp):
    new_colors = colors.copy()
    n_nodes = len(new_colors)
    random_nodes = []
    n_nodes_to_change = 1
    random_nodes = np.random.random_integers(low=0, high=n_nodes - 1, size = (n_nodes_to_change, ))
    for node in random_nodes:
        new_colors[node] = np.random.randint(low=0, high=n_max_colors)
    return new_colors

def solve_via_simulated_annealing(
    G: nx.Graph, n_max_colors: int, initial_colors: NDArrayInt, n_iters: int
):
    loss_history = np.zeros((n_iters,), dtype=np.int_)
    temp = 1000
    cur_colors = initial_colors.copy()
    cur_conflicts = number_of_conflicts(G, cur_colors)
    best_colors = initial_colors.copy()
    timer = 0
    while (timer < n_iters and temp > 0):
        rand = np.random.random()
        next_colors = tweak(cur_colors, n_max_colors, temp)
        next_conflicts = number_of_conflicts(G, next_colors)
        if (next_conflicts < cur_conflicts or
            rand > np.exp((cur_conflicts - next_conflicts) / temp)):
            cur_colors = next_colors
            cur_conflicts = next_conflicts
        k = 1
        temp -= k
        best_conflicts = number_of_conflicts(G, best_colors)
        if (cur_conflicts < best_conflicts):
            best_colors = cur_colors
            best_conflicts = cur_conflicts
        loss_history[timer] = best_conflicts
        timer += 1
    return loss_history

if __name__ == "__main__":
    seed = 42
    np.random.seed(seed)
    G = nx.erdos_renyi_graph(n=100, p=0.05, seed=seed)
    # plot_graph(G)

    n_max_iters = 1000
    n_max_colors = 3
    initial_colors = np.random.randint(low=0, high=n_max_colors - 1, size=len(G.nodes))

    loss_history = solve_via_simulated_annealing(
        G, n_max_colors, initial_colors, n_max_iters
    )
    plot_loss_history(loss_history)
