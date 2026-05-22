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

    current_colors = initial_colors.copy()
    current_loss = number_of_conflicts(G, current_colors)
    
    best_colors = current_colors.copy()
    best_loss = current_loss
    
    T = 2.0  
    alpha = 0.985  

    for i in range(n_iters):
        node_idx = np.random.randint(0, len(G.nodes))
        current_color = current_colors[node_idx]
        
        available_colors = [c for c in range(n_max_colors) if c != current_color]
        new_color = np.random.choice(available_colors) if available_colors else current_color
        
        next_colors = current_colors.copy()
        next_colors[node_idx] = new_color
        
        next_loss = number_of_conflicts(G, next_colors)
        delta_loss = next_loss - current_loss
        
        if delta_loss <= 0:
            accept = True
        else:
            accept = np.random.rand() < np.exp(-delta_loss / T)
            
        if accept:
            current_colors = next_colors
            current_loss = next_loss
            
            if current_loss < best_loss:
                best_loss = current_loss
                best_colors = current_colors.copy()
                
        loss_history[i] = current_loss
        
        T *= alpha

    set_colors(G, best_colors)

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