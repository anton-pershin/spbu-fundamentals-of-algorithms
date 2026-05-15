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


def solve_via_simulated_annealing(
    G: nx.Graph, n_max_colors: int, initial_colors: NDArrayInt, n_iters: int
) -> NDArrayInt:
    loss_history = np.zeros((n_iters,), dtype=np.int_)

    curr_colors = initial_colors.copy();
    curr_loss = number_of_conflicts(G, curr_colors)
    best_loss = curr_loss

    T = 1.0
    cooling_rate = 0.995

    for i in range(n_iters):

        new_colors = curr_colors.copy()
        vertex = np.random.randint(0, len(G.nodes))
        new_color = np.random.randint(0, n_max_colors)
        new_colors[vertex] = new_color

        new_loss = number_of_conflicts(G, new_colors)
        delta = new_loss - curr_loss

        if delta < 0 or np.random.random() < np.exp(-delta / T):
            curr_colors = new_colors
            curr_loss = new_loss
            if curr_loss < best_loss:
                best_loss = curr_loss

        loss_history[i] = best_loss
        T *= cooling_rate

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
