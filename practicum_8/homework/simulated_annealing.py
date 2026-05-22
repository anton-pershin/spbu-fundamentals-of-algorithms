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
    idx = np.random.randint(0, len(new_colors))
    current_color = new_colors[idx]
    
    shift = np.random.randint(1, n_max_colors)
    new_colors[idx] = (current_color + shift) % n_max_colors
    return new_colors

def solve_via_simulated_annealing(
    G: nx.Graph, n_max_colors: int, initial_colors: NDArrayInt, n_iters: int
) -> NDArrayInt:
    loss_history = np.zeros((n_iters,), dtype=np.int_)
    temp_history = np.zeros((n_iters,), dtype=np.float64)

    current_colors = initial_colors.copy()
    current_loss = number_of_conflicts(G, current_colors)
    
    temp_history[0] = 10
    cooling = 0.95

    for i in range(n_iters):
        proposed_colors = tweak(current_colors, n_max_colors)
        proposed_loss = sum(1 for u, v in G.edges() if proposed_colors[u] == proposed_colors[v])
        
        if i > 0:
            temp_history[i] = temp_history[i-1] * cooling
        
        delta = proposed_loss - current_loss
        if delta < 0 or np.random.random() < np.exp(-delta / max(temp_history[i], 1e-9)):
            current_colors = proposed_colors
            current_loss = number_of_conflicts(G, current_colors)
        
            
        loss_history[i] = current_loss
        

        if current_loss == 0:
            loss_history[i+1:] = 0
            break
            
    return loss_history


if __name__ == "__main__":
    seed = 42
    np.random.seed(seed)
    G = nx.erdos_renyi_graph(n=100, p=0.05, seed=seed)
    plot_graph(G)

    n_max_iters = 500
    n_max_colors = 3
    initial_colors = np.random.randint(low=0, high=n_max_colors, size=len(G.nodes))

    loss_history = solve_via_simulated_annealing(
        G, n_max_colors, initial_colors, n_max_iters
    )
    plot_loss_history(loss_history)
    print()