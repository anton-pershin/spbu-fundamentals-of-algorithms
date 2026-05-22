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

    loss_history = np.zeros(n_iters, dtype=np.int_)
    colors = initial_colors.copy() 
    current_conflicts = number_of_conflicts(G, colors)
    best_colors = colors.copy()
    best_conflicts_number = current_conflicts

    for i in range(n_iters):
        temperature = 10 * (1 - i / n_iters)

        if temperature < 0.001:
            temperature = 0.001

        bad_vertices = []

        for u, v in G.edges:
            
            if colors[u] == colors[v]:
                bad_vertices.append(u)
                bad_vertices.append(v)

        if len(bad_vertices) == 0:

            loss_history[i:] = 0
            break

        vertex = np.random.choice(bad_vertices)

        candidate = colors.copy()

        best_color = candidate[vertex]
        min_local_conflicts = float("inf")

        for color in range(n_max_colors):

            if color == candidate[vertex]:
                continue
            
            local_conflicts = 0

            for neighbor in G.neighbors(vertex):

                if colors[neighbor] == color:
                    local_conflicts += 1

            if local_conflicts < min_local_conflicts:
                min_local_conflicts = local_conflicts
                best_color = color

        candidate[vertex] = best_color

        candidate_conflicts = number_of_conflicts(G, candidate)

        diff = candidate_conflicts - current_conflicts

        accepted = (diff <= 0 or np.random.rand() < np.exp(-diff / temperature))

        if accepted:
            colors = candidate
            current_conflicts = candidate_conflicts

        if current_conflicts < best_conflicts_number:
            best_conflicts_number = current_conflicts
            best_colors = colors.copy()

        loss_history[i] = best_conflicts_number

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
