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

    loss_history = np.zeros((n_iters,), dtype=np.int_)
 
    current_colors = initial_colors.copy()
    current_loss = number_of_conflicts(G, current_colors)
 
    best_colors = current_colors.copy()
    best_loss = current_loss
 
    n_nodes = len(G.nodes)
 
    T_start = 5.0
    T_end = 0.01
    cooling_rate = (T_end / T_start) ** (1.0 / max(n_iters - 1, 1))
 
    T = T_start
 
    for i in range(n_iters):
        node_idx = np.random.randint(0, n_nodes)
        old_color = current_colors[node_idx]
 
        new_color = np.random.randint(0, n_max_colors)
        if new_color == old_color:
            new_color = (old_color + 1) % n_max_colors
 
        new_colors = current_colors.copy()
        new_colors[node_idx] = new_color
        new_loss = number_of_conflicts(G, new_colors)
 
        delta = new_loss - current_loss
        if delta < 0 or np.random.rand() < np.exp(-delta / T):
            current_colors = new_colors
            current_loss = new_loss
 
        if current_loss < best_loss:
            best_loss = current_loss
            best_colors = current_colors.copy()
 
        loss_history[i] = current_loss
 
        T *= cooling_rate
 
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
