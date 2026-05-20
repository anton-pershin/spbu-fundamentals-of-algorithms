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

    current_colors = initial_colors.copy()
    current_conflicts = number_of_conflicts(G, current_colors)
    loss_history[0] = current_conflicts
    temp = 100.0
    alpha = 0.98

    last_valid_index = 0

    for i in range(1, n_iters):
        if current_conflicts == 0:
            break
        nodes = list(G.nodes)
        random_node = np.random.choice(nodes)
        old_color = G.nodes[random_node]["color"]

        new_color = old_color
        while new_color == old_color:
            new_color = np.random.randint(low=0, high=n_max_colors)
        current_1_colors = current_colors.copy()
        current_1_colors[random_node] = new_color

        new_conflicts = number_of_conflicts(G, current_1_colors)
        difference = new_conflicts - current_conflicts
        if difference < 0 or np.random.rand() < np.exp(-difference / temp):
            current_colors = current_1_colors.copy()
            current_conflicts = new_conflicts

        temp *= alpha
        last_valid_index = i

        loss_history[i] = current_conflicts

    loss_history[last_valid_index + 1:] = current_conflicts

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
