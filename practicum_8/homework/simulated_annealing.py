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

def tweak(colors: NDArrayInt, n_max_colors: int, G: nx.Graph) -> NDArrayInt:
    new_colors = colors.copy()
    n_nodes = len(new_colors)
    set_colors(G, new_colors)
    conflicting_vertices = set()
    for node in G.nodes:
        for neighbor in G.neighbors(node):
            if G.nodes[node]["color"] == G.nodes[neighbor]["color"]:
                conflicting_vertices.add(node)
                conflicting_vertices.add(neighbor)
    if conflicting_vertices:
        random_i = np.random.choice(list(conflicting_vertices))
    else:
        return new_colors

    random_color = np.random.randint(0, n_max_colors)
    new_colors[random_i] = random_color
    return new_colors

def solve_via_simulated_annealing(
    G: nx.Graph, n_max_colors: int, initial_colors: NDArrayInt, n_iters: int
) -> NDArrayInt:
    loss_history = np.zeros((n_iters,), dtype=np.int_)
    current_colors = initial_colors.copy()
    current_conflicts = number_of_conflicts(G, current_colors)
    best_colors = current_colors.copy()
    best_conflicts = current_conflicts
    loss_history[0] = best_conflicts
    temperature = 100.0
    cooling_rate = 0.9

    for i in range(1, n_iters):
        new_colors = tweak(current_colors, n_max_colors, G)
        new_conflicts = number_of_conflicts(G, new_colors)
        delta = new_conflicts - current_conflicts
        if delta < 0 or np.random.random() < np.exp(-delta / temperature):
            current_colors = new_colors
            current_conflicts = new_conflicts
            if current_conflicts < best_conflicts:
                best_conflicts = current_conflicts
                best_colors = current_colors.copy()

        temperature *= cooling_rate
        if best_conflicts == 0:
            loss_history[i:] = best_conflicts
            break
        loss_history[i] = best_conflicts

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
