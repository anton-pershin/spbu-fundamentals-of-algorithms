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


def number_of_conflicts(G: nx.Graph, colors: NDArrayInt) -> int:

    ##########################
    ### PUT YOUR CODE HERE ###
    ##########################

    pass


def tweak(colors: NDArrayInt, n_max_colors: int) -> NDArrayInt:

    ##########################
    ### PUT YOUR CODE HERE ###
    ##########################

    pass


def tweak_optimized(colors: NDArrayInt, n_max_colors: int) -> NDArrayInt:

    ##########################
    ### PUT YOUR CODE HERE ###
    ##########################

    pass


def solve_via_hill_climbing(
    G: nx.Graph, n_max_colors: int, initial_colors: NDArrayInt, n_iters: int
) -> NDArrayInt:

    ##########################
    ### PUT YOUR CODE HERE ###
    ##########################

    pass


def solve_via_random_search(
    G: nx.Graph, n_max_colors: int, initial_colors: NDArrayInt, n_iters: int
) -> NDArrayInt:

    ##########################
    ### PUT YOUR CODE HERE ###
    ##########################

    pass


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
