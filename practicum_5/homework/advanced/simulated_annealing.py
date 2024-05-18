import numpy as np
from numpy.typing import NDArray
import networkx as nx
import math

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

def tweak1(colors, n_max_colors):
    new_colors = colors.copy()
    n_nodes = len(new_colors)
    random_i = np.random.randint(low=0, high=n_nodes)
    random_color = np.random.randint(low=0, high=n_max_colors)
    new_colors[random_i] = random_color
    return new_colors

def tweak(colors, n_max_colors):
    new_colors = colors.copy()
    random_node = np.random.choice(list(G.nodes()))
    neighbors = list(G.neighbors(random_node))
    value_counts = {value: sum(1 for node in neighbors if G.nodes[node]['color'] == value) for value in range(3)}
    least_common_value = min(value_counts, key=value_counts.get)
    new_colors[random_node] = least_common_value
    return new_colors



def solve_via_simulated_annealing1(
    G: nx.Graph, n_max_colors: int, initial_colors: NDArrayInt, n_iters: int
):
    loss_history = np.zeros((n_iters,), dtype=np.int_) 
    current_colors = initial_colors 
    current_loss = number_of_conflicts(G, current_colors) 
    t_start = 100 
    t_min = 0.0001 
    k = 0.1
    for i in range(n_iters):
        t_start = max(t_start * k, t_min)
        new_colors = tweak(current_colors, n_max_colors)
        new_loss = number_of_conflicts(G, new_colors)
        delta_loss = new_loss - current_loss

        if delta_loss < 0 or np.random.rand() < np.exp(-delta_loss / t_start):
            current_colors = new_colors
            current_loss = new_loss

        loss_history[i] = current_loss
    set_colors(G, current_colors)
    return loss_history


def solve_via_simulated_annealing(
    G: nx.Graph, n_max_colors: int, initial_colors: NDArrayInt, n_iters: int):
    loss_history = np.zeros((n_iters,), dtype=np.int_)
    cur_colors = initial_colors.copy()
    next_colors = initial_colors.copy()
    next_best_colors = initial_colors.copy()
    n_tweaks = 10
    for i in range(n_iters):
        cur_loss = number_of_conflicts(G, cur_colors)
        loss_history[i] = number_of_conflicts(G, cur_colors)
        next_best_colors = tweak(cur_colors, n_max_colors)
        next_best_loss = number_of_conflicts(G, next_best_colors)
        for _ in range(n_tweaks):
            next_colors = tweak(cur_colors, n_max_colors)
            next_loss = number_of_conflicts(G, next_colors)
            next_rng = np.random.default_rng().random()
            if (_ != 1 and _ != 0):
                next_t = 1 / np.log(_)
            else:
                next_t = 1
            next_exp = math.exp((next_best_loss - next_loss) / next_t)
            if next_loss < next_best_loss or next_rng < next_exp:
                next_best_colors = next_colors
                next_best_loss = number_of_conflicts(G, next_best_colors)
        cur_rng = np.random.default_rng().random()
        if (i != 1 and i != 0):
            cur_t = 1 / np.log(i)
        else:
            cur_t = 1
        cur_exp = math.exp((next_best_loss - cur_loss) / cur_t)
        if (next_best_loss < cur_loss or cur_rng < cur_exp):
            cur_colors = next_best_colors
        if (loss_history[i] == max(set(loss_history), key=list(loss_history).count)):
            return loss_history

    return loss_history


if __name__ == "__main__":
    seed = 42
    np.random.seed(seed)
    G = nx.erdos_renyi_graph(n=100, p=0.05, seed=seed)
    plot_graph(G)

    n_max_iters = 100
    n_max_colors = 3
    initial_colors = np.random.randint(low=0, high=n_max_colors - 1, size=len(G.nodes))

    loss_history = solve_via_simulated_annealing(
        G, n_max_colors, initial_colors, n_max_iters
    )
    plot_loss_history(loss_history)
