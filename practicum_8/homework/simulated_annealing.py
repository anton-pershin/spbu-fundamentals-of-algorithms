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
    vertex = np.random.randint(0, len(colors))
    current_color = colors[vertex]
    available = [c for c in range(n_max_colors) if c != current_color]
    new_colors[vertex] = np.random.choice(available)
    return new_colors


def temperature_schedule(t: int, n_iters: int, T0: float = 50.0, T_min: float = 0.05) -> float:
    return T0 * (T_min / T0) ** (t / max(n_iters - 1, 1))


def solve_via_simulated_annealing(
    G: nx.Graph, n_max_colors: int, initial_colors: NDArrayInt, n_iters: int
) -> NDArrayInt:
    loss_history = np.zeros((n_iters,), dtype=np.int_)

    current_colors = initial_colors.copy()
    current_loss = number_of_conflicts(G, current_colors)

    best_colors = current_colors.copy()
    best_loss = current_loss

    for t in range(n_iters):
        T = temperature_schedule(t, n_iters)

        candidate_colors = tweak(current_colors, n_max_colors)
        candidate_loss = number_of_conflicts(G, candidate_colors)

        delta = candidate_loss - current_loss

        if delta < 0 or np.random.rand() < np.exp(-delta / T):
            current_colors = candidate_colors
            current_loss = candidate_loss

        if current_loss < best_loss:
            best_colors = current_colors.copy()
            best_loss = current_loss

        loss_history[t] = best_loss

        if best_loss == 0:
            loss_history[t:] = 0
            break

    set_colors(G, best_colors)
    print(f"Best number of conflicts: {best_loss}")

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
    plot_loss_history(loss_history)

    node_weights = {n: G.nodes[n]["color"] for n in G.nodes}
    plot_graph(G, node_weights=node_weights)
    print()