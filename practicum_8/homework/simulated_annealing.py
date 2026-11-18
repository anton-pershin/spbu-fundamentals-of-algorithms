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

    n_nodes = len(G.nodes)
    nodes = list(G.nodes)
    index = {n: i for i, n in enumerate(nodes)}
    neighbors = [[index[m] for m in G.neighbors(n)] for n in nodes]

    colors = initial_colors.copy()
    n_conflicts = number_of_conflicts(G, colors)

    t_start, t_end = 1.0, 0.02
    alpha = (t_end / t_start) ** (1.0 / max(n_iters - 1, 1))
    temperature = t_start

    n_moves_per_iter = 10

    for i in range(n_iters):
        loss_history[i] = n_conflicts

        for _ in range(n_moves_per_iter):
            conflicting = [
                v for v in range(n_nodes)
                if any(colors[v] == colors[u] for u in neighbors[v])
            ]
            if conflicting:
                v = conflicting[np.random.randint(len(conflicting))]
            else:
                v = np.random.randint(n_nodes)

            new_color = np.random.randint(n_max_colors - 1)
            if new_color >= colors[v]:
                new_color += 1

            old_local = sum(colors[v] == colors[u] for u in neighbors[v])
            new_local = sum(new_color == colors[u] for u in neighbors[v])
            delta = new_local - old_local

            if delta <= 0 or np.random.rand() < np.exp(-delta / temperature):
                colors[v] = new_color
                n_conflicts += delta

        temperature *= alpha

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
