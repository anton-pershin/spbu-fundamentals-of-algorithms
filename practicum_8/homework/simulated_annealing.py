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


def tweak(
    colors: NDArrayInt,
    n_max_colors: int,
    idx: int,
    neighbors_idx: list[list[int]],
    greedy_prob: float = 0.7,
) -> NDArrayInt:
    new_colors = colors.copy()
    if np.random.rand() < greedy_prob:
        # Жадный выбор: цвет, минимизирующий число конфликтов с соседями
        new_colors[idx] = min(
            range(n_max_colors),
            key=lambda c: sum(1 for k in neighbors_idx[idx] if colors[k] == c),
        )
    else:
        # Случайный выбор для сохранения "разведки"
        new_colors[idx] = np.random.randint(n_max_colors)
    return new_colors


def temperature_schedule(iteration: int, n_iters: int, T0: float = 5.0, T_min: float = 0.005) -> float:
    alpha = (T_min / T0) ** (1 / n_iters)
    return T0 * (alpha ** iteration)


def solve_via_simulated_annealing(
    G: nx.Graph, n_max_colors: int, initial_colors: NDArrayInt, n_iters: int
) -> NDArrayInt:
    loss_history = np.zeros((n_iters,), dtype=np.int_)

    nodes = list(G.nodes)
    node_index = {node: i for i, node in enumerate(nodes)}
    neighbors_idx = [[node_index[m] for m in G.neighbors(node)] for node in nodes]
    n_nodes = len(nodes)

    cur_colors = initial_colors.copy()
    cur_loss = number_of_conflicts(G, cur_colors)

    for i in range(n_iters):
        loss_history[i] = cur_loss
        T = temperature_schedule(i, n_iters)

        # Выбираем случайную вершину среди конфликтующих (если такие есть)
        conflicting = [
            j for j in range(n_nodes)
            if any(cur_colors[j] == cur_colors[k] for k in neighbors_idx[j])
        ]
        idx = conflicting[np.random.randint(len(conflicting))] if conflicting else np.random.randint(n_nodes)

        next_colors = tweak(cur_colors, n_max_colors, idx, neighbors_idx)
        next_loss = number_of_conflicts(G, next_colors)

        delta = next_loss - cur_loss
        if delta <= 0 or np.random.rand() < np.exp(-delta / max(T, 1e-9)):
            cur_colors, cur_loss = next_colors, next_loss

    set_colors(G, cur_colors)
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
