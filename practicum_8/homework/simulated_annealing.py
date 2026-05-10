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
    n_nodes = len(new_colors)
    random_i = np.random.randint(0, n_nodes)
    random_color = np.random.randint(0, n_max_colors)
    new_colors[random_i] = random_color
    return new_colors


def solve_via_simulated_annealing(
    G: nx.Graph, n_max_colors: int, initial_colors: NDArrayInt, n_iters: int
) -> NDArrayInt:
    loss_history = np.zeros((n_iters,), dtype=np.int_)

    cur_colors = initial_colors
    cur_conf = number_of_conflicts(G, cur_colors)

    best_colors = cur_colors
    best_conf = cur_conf
    
    loss_history[0] = best_conf
    T = 1.0
    cooling_rate = 0.95

    for i in range(1, n_iters):
        T = T * cooling_rate

        new_colors = tweak(cur_colors, n_max_colors)
        new_conf = number_of_conflicts(G, new_colors)
    
        delt = new_conf - cur_conf
        if delt < 0:
            deci = True
        else:
            chance = np.exp(-delt/T)
            deci = chance > np.random.random() 

        if deci:
            cur_colors = new_colors
            cur_conf = new_conf
        
            if cur_conf < best_conf:
                best_colors = cur_colors
                best_conf = cur_conf
        
        loss_history[i] = best_conf
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
