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

def greedy_tweak(G: nx.Graph, colors: NDArrayInt, n_max_colors: int) -> NDArrayInt:
    new_colors = colors.copy()
    set_colors(G, new_colors)

    conflicting = set()
    for u, v in G.edges:
        if G.nodes[u]["color"] == G.nodes[v]["color"]:
            conflicting.add(u)
            conflicting.add(v)

    if conflicting and np.random.random() < 0.8:
        vertex = np.random.choice(list(conflicting))
    else:
        vertex = np.random.choice(list(G.nodes))

    best_colors = []
    best_local_conflicts = float('inf')
    old_color = new_colors[vertex]

    for color in range(n_max_colors):
        new_colors[vertex] = color
        set_colors(G, new_colors)
        local_conflicts = 0
        for neighbor in G.neighbors(vertex):
            if G.nodes[vertex]["color"] == G.nodes[neighbor]["color"]:
                local_conflicts += 1

        if local_conflicts < best_local_conflicts:
            best_local_conflicts = local_conflicts
            best_colors = [color]
        elif local_conflicts == best_local_conflicts:
            best_colors.append(color)

    new_colors[vertex] = old_color
    new_colors[vertex] = np.random.choice(best_colors)
    return new_colors

def solve_via_simulated_annealing(
    G: nx.Graph, n_max_colors: int, initial_colors: NDArrayInt, n_iters: int
) -> NDArrayInt:
    loss_history = np.zeros((n_iters,), dtype=np.int_)

    current_colors = initial_colors.copy()
    current_conflicts = number_of_conflicts(G, current_colors)
    best_colors = current_colors.copy()
    best_conflicts = current_conflicts
    loss_history[0] = best_conflicts

    T_start = 100.0
    T_end = 0.01
    cooling_rate = (T_end / T_start) ** (1.0 / n_iters)
    T = T_start

    for i in range(1, n_iters):
        new_colors = greedy_tweak(G, current_colors, n_max_colors)
        new_conflicts = number_of_conflicts(G, new_colors)

        delta = new_conflicts - current_conflicts

        if delta < 0 or np.random.random() < np.exp(-delta / T):
            current_colors = new_colors
            current_conflicts = new_conflicts
            if current_conflicts < best_conflicts:
                best_conflicts = current_conflicts
                best_colors = current_colors.copy()

        loss_history[i] = best_conflicts
        T *= cooling_rate

        if best_conflicts == 0:
            loss_history[i + 1:] = 0
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
