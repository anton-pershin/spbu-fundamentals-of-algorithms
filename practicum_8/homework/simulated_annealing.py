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
    
    loss_history[0] = current_loss
    
    T_start = 100.0

    T_end = 0.1
    
    cooling_rate = (T_end / T_start) ** (1.0 / n_iters)
    
    T = T_start
    
    for i in range(1, n_iters):

        node_to_recolor = np.random.choice(len(G.nodes))
        
        if np.random.random() < 0.2:
            new_color = np.random.randint(0, n_max_colors)
        else:
            neighbors = list(G.neighbors(node_to_recolor))
            
            if neighbors:
                neighbor_colors = set()
                for neighbor in neighbors:
                    neighbor_colors.add(current_colors[neighbor])
                
                all_colors = set(range(n_max_colors))
                available_colors = all_colors - neighbor_colors
                
                if available_colors:
                    new_color = np.random.choice(list(available_colors))
                else:
                    new_color = np.random.randint(0, n_max_colors)
            else:
                new_color = np.random.randint(0, n_max_colors)
        
        new_colors = current_colors.copy()
        new_colors[node_to_recolor] = new_color
        
        new_loss = number_of_conflicts(G, new_colors)
        delta_loss = new_loss - current_loss
        
        if delta_loss < 0:
            current_colors = new_colors
            current_loss = new_loss
        else:
            if np.random.random() < np.exp(-delta_loss / T):
                current_colors = new_colors
                current_loss = new_loss
        
        if current_loss < best_loss:
            best_colors = current_colors.copy()
            best_loss = current_loss

        loss_history[i] = best_loss
        
        T *= cooling_rate
    
    set_colors(G, best_colors)
    
    print(f"Начальное количество конфликтов: {number_of_conflicts(G, initial_colors)}")
    print(f"Лучшее найденное количество конфликтов: {best_loss}")
    print(f"Итоговая температура: {T:.6f}")

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
   