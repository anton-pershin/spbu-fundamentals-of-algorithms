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

    class TemperatureSchedule:
        def __init__(self, initial_temp: float = 1.0, min_temp: float = 1e-4):
            self.initial_temp = float(initial_temp)
            self.min_temp = float(min_temp)

        def __call__(self, iteration: int, max_iterations: int) -> float:
            if max_iterations <= 1:
                return self.initial_temp
            progress = iteration / float(max_iterations - 1)
            temperature = self.initial_temp * (1.0 - progress)
            return max(self.min_temp, temperature)

    class TweakOperator:
        def __init__(self, n_colors: int):
            self.n_colors = int(n_colors)

        def __call__(self, colors: NDArrayInt, conflict_indices: np.ndarray) -> NDArrayInt:
            candidate = None
            if len(conflict_indices) > 0 and np.random.rand() < 0.85:
                candidate = np.random.choice(conflict_indices)
            else:
                candidate = np.random.randint(0, len(colors))

            current_color = int(colors[candidate])
            choices = [c for c in range(self.n_colors) if c != current_color]
            if not choices:
                return colors.copy()

            proposal = colors.copy()
            proposal[candidate] = np.random.choice(choices)
            return proposal

    def get_conflict_indices(graph: nx.Graph, colors: NDArrayInt) -> np.ndarray:
        node_index = {node: idx for idx, node in enumerate(graph.nodes)}
        conflicts = set()
        for u, v in graph.edges:
            if colors[node_index[u]] == colors[node_index[v]]:
                conflicts.add(node_index[u])
                conflicts.add(node_index[v])
        return np.fromiter(conflicts, dtype=np.int_, count=len(conflicts))

    current_colors = initial_colors.copy().astype(np.int_)
    set_colors(G, current_colors)
    current_loss = number_of_conflicts(G, current_colors)
    best_colors = current_colors.copy()
    best_loss = int(current_loss)

    schedule = TemperatureSchedule(initial_temp=1.0, min_temp=1e-4)
    tweak = TweakOperator(n_max_colors)

    for iteration in range(n_iters):
        conflict_indices = get_conflict_indices(G, current_colors)
        proposed_colors = tweak(current_colors, conflict_indices)

        set_colors(G, proposed_colors)
        proposed_loss = number_of_conflicts(G, proposed_colors)

        delta = int(proposed_loss) - int(current_loss)
        temperature = schedule(iteration, n_iters)
        accept_probability = np.exp(-delta / temperature) if delta > 0 else 1.0

        if delta <= 0 or np.random.rand() < accept_probability:
            current_colors = proposed_colors
            current_loss = proposed_loss

        if current_loss < best_loss:
            best_loss = int(current_loss)
            best_colors = current_colors.copy()

        loss_history[iteration] = best_loss

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
