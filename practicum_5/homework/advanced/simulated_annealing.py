import numpy as np
from numpy.typing import NDArray
import networkx as nx
from math import pow

from src.plotting import plot_graph
#from src.plotting import plot_loss_history


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


def tweak(colors, n_max_colors):
    new_colors = colors.copy()
    n_nodes = len(new_colors)
    random_i = np.random.randint(low=0, high=n_nodes)
    random_color = np.random.randint(low=0, high=n_max_colors)
    new_colors[random_i] = random_color
    
    return new_colors


def solve_via_simulated_annealing(
    G: nx.Graph, n_max_colors: int, initial_colors: NDArrayInt, n_iters: int
):
    global probability
    loss_history = np.zeros((n_iters,), dtype=np.int_)
    

    cur_colors = initial_colors
    best_colors = initial_colors.copy()
    
    temperature = 1000

    
    for i in range(0, n_iters):            
        loss_history[i] = number_of_conflicts(G, cur_colors)
        
        best_colors = tweak(cur_colors, n_max_colors)
        n_conflicts_best = number_of_conflicts(G, best_colors)
        

        diff_conflicts = loss_history[i] - n_conflicts_best
        if diff_conflicts > 0:
            cur_colors = best_colors
            loss_history[i] = n_conflicts_best
        else:
            if temperature > 0.0000001:
                r = np.random.rand()
                if i == 0:
                    h = 1 / (1 + np.exp(abs(diff_conflicts)/(i+1)) )
                else:
                    h = 1 / (1 + np.exp(abs(diff_conflicts)/i) )
                if h >= r:
                    cur_colors = best_colors
                    loss_history[i] = n_conflicts_best

        temperature *= np.exp(-0.9 * pow(i, 1 / n_max_colors))

        if temperature < 0.0000001:
            temperature = 0

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
   # plot_loss_history(loss_history)