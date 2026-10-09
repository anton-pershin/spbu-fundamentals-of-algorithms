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
    idx = np.random.randint(len(new_colors))
    possible = [c for c in range(n_max_colors) if c != new_colors[idx]]
    if possible:
        new_colors[idx] = np.random.choice(possible)
    return new_colors

def temperature_schedule(iter_idx: int, n_iters: int) -> float:
    T0 = 1.0
    T_min = 0.01
    alpha = (T_min / T0) ** (1.0 / max(1, n_iters - 1))
    return T0 * (alpha ** iter_idx)

def solve_via_simulated_annealing(
    G: nx.Graph, n_max_colors: int, initial_colors: NDArrayInt, n_iters: int
) -> NDArrayInt:
    loss_history = np.zeros((n_iters,), dtype=np.int_)

    current_colors = initial_colors.copy()
    current_conflicts = number_of_conflicts(G, current_colors)

    best_colors = current_colors.copy()
    best_conflicts = current_conflicts

    for i in range(n_iters):
        T = temperature_schedule(i, n_iters)

        candidate_colors = tweak(current_colors, n_max_colors)
        candidate_conflicts = number_of_conflicts(G, candidate_colors)

        delta = candidate_conflicts - current_conflicts

        if delta <= 0 or np.random.rand() < np.exp(-delta / max(T, 1e-12)):
            current_colors = candidate_colors
            current_conflicts = candidate_conflicts

            if current_conflicts < best_conflicts:
                best_colors = current_colors.copy()
                best_conflicts = current_conflicts

        loss_history[i] = current_conflicts

    set_colors(G, best_colors)
    return loss_history

if __name__ == "__main__":
    seed = 42
    np.random.seed(seed)
    G = nx.erdos_renyi_graph(n=100, p=0.05, seed=seed)
    plot_graph(G)

    n_max_iters = 500
    n_max_colors = 3
    initial_colors = np.random.randint(low=0, high=n_max_colors, size=len(G.nodes))

    loss_history = solve_via_simulated_annealing(
        G, n_max_colors, initial_colors, n_max_iters
    )
    plot_loss_history(loss_history)
    print()