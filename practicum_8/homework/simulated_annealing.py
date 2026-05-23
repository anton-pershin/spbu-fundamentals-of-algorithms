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
    vertex_idx = np.random.randint(0, len(colors))
    current_color = new_colors[vertex_idx]
    
    possible_colors = list(range(n_max_colors))
    possible_colors.remove(current_color)
    new_color = np.random.choice(possible_colors)
    new_colors[vertex_idx] = new_color
    
    return new_colors


def simulated_annealing_schedule(iteration: int, n_iters: int) -> float:
    T_start = 1.0
    T_end = 0.01
    return T_start * (T_end / T_start) ** (iteration / n_iters)


def solve_via_simulated_annealing(
    G: nx.Graph, n_max_colors: int, initial_colors: NDArrayInt, n_iters: int
) -> NDArrayInt:
    loss_history = np.zeros((n_iters,), dtype=np.int_)
    
    current_colors = initial_colors.copy()
    current_loss = number_of_conflicts(G, current_colors)
    best_colors = current_colors.copy()
    best_loss = current_loss
    
    loss_history[0] = current_loss
    
    for iteration in range(1, n_iters):

        candidate_colors = tweak(current_colors, n_max_colors)
        candidate_loss = number_of_conflicts(G, candidate_colors)
        
        delta = candidate_loss - current_loss
        temperature = simulated_annealing_schedule(iteration, n_iters)
        
        if delta < 0:
            accept = True
        else:
            acceptance_probability = np.exp(-delta / temperature)
            accept = np.random.random() < acceptance_probability
        
        if accept:
            current_colors = candidate_colors
            current_loss = candidate_loss
            
            if current_loss < best_loss:
                best_colors = current_colors.copy()
                best_loss = current_loss
        
        loss_history[iteration] = best_loss
        
        if best_loss == 0:
            loss_history[iteration:] = best_loss
            break
    
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
    print(f"Final number of conflicts: {loss_history[-1]}")
    print(f"Best coloring found with {n_max_colors} colors")