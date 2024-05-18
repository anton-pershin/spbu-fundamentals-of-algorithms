import numpy as np
from numpy.typing import NDArray
import networkx as nx

from src.plotting import plot_graph, plot_loss_history


NDArrayInt = NDArray[np.int_]


def number_of_conflicts(G, colors):
    set_colors(G, colors)
    n = 0
    for n_in, n_out in G.edges:
        if G.nodes[n_in]["color"] == G.nodes[n_out]["color"]:
            n += 1
    return n


def set_colors(G, colors):
    for n, color in zip(G.nodes, colors):
        G.nodes[n]["color"] = color


def tweak(colors, n_max_colors, temp):
    new_colors = colors.copy()
    n_nodes = len(new_colors)
    random_nodes = []
    n_nodes_to_change = 1
    random_nodes = np.random.random_integers(low=0, high=n_nodes - 1, size = (n_nodes_to_change, ))
    for node in random_nodes:
        new_colors[node] = np.random.randint(low=0, high=n_max_colors)
    return new_colors


def solve_via_simulated_annealing(
    G: nx.Graph, n_max_colors: int, initial_colors: NDArrayInt, n_iters: int
):
    loss_history = np.zeros((n_iters,), dtype=np.int_)
    temp = 500
    now_colors=initial_colors.copy()
    now_conflict=number_of_conflicts(G,now_colors)
    best_colors=initial_colors.copy()
    timer=0
    while (timer < n_iters and temp > 0):
        rand=np.random.random()
        next_col=tweak(now_colors,n_max_colors,temp)
        next_conflicts=number_of_conflicts(G,next_col)
        if (next_conflicts <  now_conflict or rand > np.exp((now_conflict-next_conflicts)/temp)):
            now_colors=next_col
            now_conflict=next_conflicts
        k=1
        temp-=k
        best_conflict=number_of_conflicts(G,best_colors)
        if (now_conflict < best_conflict):
            best_colors=now_colors
            best_conflict=now_conflict
        loss_history[timer]=best_conflict
        timer+=1
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