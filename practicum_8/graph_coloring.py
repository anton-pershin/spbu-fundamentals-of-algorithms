from typing import Protocol

import numpy as np
import networkx as nx

from src.common import NDArrayInt
from src.plotting.graphs import plot_graph
from src.plotting.misc import plot_loss_history


class GraphColoringSolver(Protocol):
    def __call__(
        G: nx.Graph, n_max_colors: int, initial_colors: NDArrayInt, n_iters: int
    ) -> NDArrayInt:
        pass

def set_colors(G: nx.Graph, colors: NDArrayInt) -> None:
    for node, color in zip(G.nodes, colors):
        G.nodes[node]["color"] = color

def number_of_conflicts(G: nx.Graph, colors: NDArrayInt) -> int:
    set_colors(G, colors)
    n_conflicts = 0
    for node in G.nodes:
        for neighbor in G.neighbors(node):
            if G.nodes[node]["color"] == G.nodes[neighbor]["color"]:
                n_conflicts += 1
    return n_conflicts


def tweak(colors: NDArrayInt, n_max_colors: int) -> NDArrayInt:
    new_colors = colors.copy()
    n_nodes = len(new_colors)
    random_i = np.random.randint(0, n_nodes)
    random_color = np.random.randint(0, n_max_colors)
    new_colors[random_i] = random_color
    return new_colors


def tweak_optimized(colors: NDArrayInt, n_max_colors: int) -> NDArrayInt:

    pass

def solve_via_hill_climbing(
    G: nx.Graph, n_max_colors: int, initial_colors: NDArrayInt, n_iters: int
) -> NDArrayInt:
    n_tweaks = 10
    loss_history = np.zeros((n_iters, ), dtype=np.int_)
    best_conflicts = number_of_conflicts(G, initial_colors)
    best_colors = initial_colors
    loss_history[0] = best_conflicts
    for i in range(1, n_iters):
        for _ in range(n_tweaks):
            colors = tweak(best_colors, n_max_colors)
            n_conflicts = number_of_conflicts(G, colors)
            if n_conflicts < best_conflicts:
                best_conflicts = n_conflicts
                best_colors = colors
        loss_history[i] = best_conflicts
    return loss_history


def solve_via_random_search(
    G: nx.Graph, n_max_colors: int, initial_colors: NDArrayInt, n_iters: int
) -> NDArrayInt:
    loss_history = np.zeros((n_iters, ), dtype=np.int_)
    best_conflicts = number_of_conflicts(G, initial_colors)
    best_colors = initial_colors
    loss_history[0] = best_conflicts
    for i in range(1, n_iters):
        colors = np.random.randint(low=0, high=n_max_colors - 1, size=len(G.nodes))
        n_conflicts = number_of_conflicts(G, colors)
        if n_conflicts < best_conflicts:
            best_conflicts = n_conflicts
            best_colors = colors
        loss_history[i] = best_conflicts
    return loss_history


def solve_with_restarts(
    solver: GraphColoringSolver,
    G: nx.Graph,
    n_max_colors: int,
    initial_colors: NDArrayInt,
    n_iters: int,
    n_restarts: int,
) -> NDArrayInt:

    ##########################
    ### PUT YOUR CODE HERE ###
    ##########################

    pass


if __name__ == "__main__":
    seed = 42
    np.random.seed(seed)
    G = nx.erdos_renyi_graph(n=100, p=0.05, seed=seed)
    plot_graph(G)

    n_max_iters = 500
    n_max_colors = 3
    initial_colors = np.random.randint(low=0, high=n_max_colors - 1, size=len(G.nodes))

    loss_history = solve_via_random_search(G, n_max_colors, initial_colors, n_max_iters)
    plot_loss_history(loss_history)

    loss_history = solve_via_hill_climbing(G, n_max_colors, initial_colors, n_max_iters)
    plot_loss_history(loss_history)

    n_restarts = 10
    loss_history = solve_with_restarts(
        solve_via_hill_climbing,
        G,
        n_max_colors,
        initial_colors,
        n_max_iters,
        n_restarts,
    )
    plot_loss_history(loss_history)
    print()
