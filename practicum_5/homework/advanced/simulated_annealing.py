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

def tweak(G:nx.Graph, colors, n_max_colors): #работает верно
    tweak_colors = colors.copy()
    tweak_node = np.random.randint(len(colors)-1)

    for i in nx.neighbors(G, tweak_node):
        tweak_color = colors[i]
        while tweak_color == colors[tweak_node]:
            tweak_color = np.random.randint(n_max_colors)
        tweak_colors[i] = tweak_color

    return tweak_colors

def transition_probability(delta, current_t):
    if delta < 0:
        return 1
    if current_t <= 0:
        return 0
    return np.exp(-1 * delta / current_t)


def solve_via_simulated_annealing(
    G: nx.Graph, n_max_colors: int, initial_colors: NDArrayInt, n_iters: int
):
    current_colors = initial_colors.copy()
    current_conflicts = number_of_conflicts(G, current_colors)
    MAX_T = 500
    rate = 0.95
    current_t = MAX_T
    counter = 0
    loss_history = np.zeros((n_iters,), dtype=np.int_)

    for _ in range(n_iters):
        new_colors = tweak(G, current_colors, n_max_colors)
        new_conflicts = number_of_conflicts(G, new_colors)
        delta = new_conflicts - current_conflicts

        if transition_probability(delta, current_t) >= np.random.random():
            current_colors = new_colors.copy()
            current_conflicts = new_conflicts
            loss_history[counter] = current_conflicts
            counter += 1

        current_t *= rate
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
    #print(ans) - количество конфликтов = 9
    plot_loss_history(loss_history)




