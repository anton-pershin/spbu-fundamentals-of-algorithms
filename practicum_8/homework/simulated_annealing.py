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


def tweak(colors: NDArrayInt, n_max_colors: int):
    new_colors = colors.copy()
    vertex = np.random.randint(0, len(new_colors))
    old_color = new_colors[vertex]
    new_colors[vertex] = np.random.randint(0, n_max_colors)
    while new_colors[vertex] == old_color:
        new_colors[vertex] = np.random.randint(0, n_max_colors)
    return new_colors, vertex, old_color, new_colors[vertex]


def temperature_schedule(initial_temperature: float, cooling_rate: float, max_steps: int):
    current_temperature = initial_temperature
    for _ in range(max_steps):
        if current_temperature < 0.0001:
            break
        yield current_temperature
        current_temperature *= cooling_rate


def solve_via_simulated_annealing(
    G: nx.Graph, n_max_colors: int, initial_colors: NDArrayInt, n_iters: int
) -> NDArrayInt:
    loss_history = np.zeros((n_iters,), dtype=np.int_)

    current_colors = initial_colors.copy()
    current_conflicts = number_of_conflicts(G, current_colors)
    best_conflicts = current_conflicts
    loss_history[0] = current_conflicts

    initial_temperature = 10.0
    cooling_rate = 0.98
    best_colors = current_colors.copy()

    temperature_generator = temperature_schedule(
        initial_temperature=initial_temperature, 
        cooling_rate=cooling_rate, 
        max_steps=n_iters - 1
    )
    for iteration_index, current_temperature in enumerate(temperature_generator, start=1):
        new_colors, vertex_index, old_color, new_color = tweak(current_colors, n_max_colors)

        conflicts_delta = 0
        for neighbor in G.neighbors(vertex_index):
            neighbor_color = current_colors[neighbor]
            if neighbor_color == old_color:
                conflicts_delta -= 1
            elif neighbor_color == new_color:
                conflicts_delta += 1
        
        new_conflicts = current_conflicts + conflicts_delta

        should_accept = (conflicts_delta < 0) or (np.random.random() < np.exp(-conflicts_delta / current_temperature))

        if should_accept:
            current_colors[vertex_index] = new_color
            current_conflicts = new_conflicts
        
        if current_conflicts < best_conflicts:
            best_colors = current_colors.copy()
            best_conflicts = current_conflicts
        
        loss_history[iteration_index] = best_conflicts

        if best_conflicts == 0:
            loss_history[iteration_index:] = 0
            break

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
