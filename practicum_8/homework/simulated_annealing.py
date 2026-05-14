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

    cur_colors=initial_colors.copy()
    cur_conflicts=number_of_conflicts(G,cur_colors)
    loss_history[0]=cur_conflicts
    temperature=10
    alpha=0.99
    for i in range(1,n_iters):
        new_colors=cur_colors.copy()
        v=np.random.randint(0, len(G.nodes))
        color=np.random.randint(0,n_max_colors)
        new_colors[v]=color
        new_conflicts=number_of_conflicts(G,new_colors)
        if new_conflicts<=cur_conflicts:
            cur_conflicts=new_conflicts
            cur_colors=new_colors
        else:
            r = np.random.random()
            if r<np.exp((cur_conflicts-new_conflicts) / temperature):
                cur_conflicts = new_conflicts
                cur_colors = new_colors
        loss_history[i] = cur_conflicts
        temperature = temperature * alpha
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
