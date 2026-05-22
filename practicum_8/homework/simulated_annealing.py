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
    new_colors = colors.copy()
    idx = np.random.randint(0, len(colors))
    old_c = new_colors[idx]
    new_c = np.random.randint(0, n_max_colors)

    while new_c == old_c:
        new_c = np.random.randint(0, n_max_colors)
    new_colors[idx] = new_c
    return new_colors

def cooling_schedule(initial_temp: float, i: int) -> float:
    return initial_temp * (0.995 ** i)

def solve_via_simulated_annealing(
    G: nx.Graph, n_max_colors: int, initial_colors: NDArrayInt, n_iters: int
) -> NDArrayInt:
    loss_history = np.zeros((n_iters,), dtype=np.int_)
    
    T_start = 10.0

    current_colors = initial_colors.copy()
    current_loss = number_of_conflicts(G, current_colors)

    best_colors = current_colors.copy()
    best_loss = current_loss

    for i in range(n_iters):
        T = cooling_schedule(T_start, i)
        candidate = tweak(current_colors, n_max_colors)
        candidate_loss = number_of_conflicts(G, candidate)

        dE = candidate_loss - current_loss

        if dE < 0 or np.random.random() < np.exp(-dE / T):
            current_colors = candidate
            current_loss = candidate_loss

        if current_loss < best_loss:
            best_loss = current_loss
            best_colors = current_colors.copy()

        loss_history[i] = current_loss

        if best_loss == 0:
            loss_history[i:] = 0
            break

    set_colors(G, best_colors)

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
