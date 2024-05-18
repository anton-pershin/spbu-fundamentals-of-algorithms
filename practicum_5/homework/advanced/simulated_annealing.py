import numpy as np
from numpy.typing import NDArray
import networkx as nx

from typing import Union, Any
import matplotlib.pyplot as plt
#from src.plotting import plot_graph, plot_loss_history


NDArrayInt = NDArray[np.int_]

#Copied code from src.plotting
def plot_loss_history(
    loss_history: NDArrayInt, xlabel="# iterations", ylabel="# conflicts"
) -> None:
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    if loss_history.ndim == 1:
        loss_history = loss_history.reshape(1, -1)
    n_restarts, n_iters = loss_history.shape
    for i in range(n_restarts):
        ax.plot(range(n_iters), loss_history[i, :])
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid()
    fig.tight_layout()
    plt.show()

def plot_graph(
    G: Union[nx.Graph, nx.DiGraph], highlighted_edges: list[tuple[Any, Any]] = None
) -> None:
    fig, ax = plt.subplots(figsize=(12, 6))
    pos = nx.spring_layout(G)
    edge_color_list = ["black"] * len(G.edges)
    if highlighted_edges:
        for i, edge in enumerate(G.edges()):
            if edge in highlighted_edges or (edge[1], edge[0]) in highlighted_edges:
                edge_color_list[i] = "red"
    options = dict(
        font_size=12,
        node_size=500,
        node_color="white",
        edgecolors="black",
        edge_color=edge_color_list,
    )
    nx.draw_networkx(G, pos, ax=ax, **options)
    if nx.is_weighted(G):
        labels = {e: G.edges[e]["weight"] for e in G.edges}
        nx.draw_networkx_edge_labels(G, pos, ax=ax, edge_labels=labels)
    plt.show()

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

def tweak(colors, n_max_colors):
    new_colors = colors.copy()
    n_nodes = len(new_colors)
    random_ind = np.random.randint(low=0, high=n_nodes)
    random_color = np.random.randint(low=0, high=n_max_colors)
    new_colors[random_ind] = random_color
    return new_colors

def solve_via_simulated_annealing(
    G: nx.Graph, n_max_colors: int, initial_colors: NDArrayInt, n_iters: int
):
    loss_history = np.zeros((n_iters,), dtype=np.int_)
    current_colors = initial_colors.copy()
    current_loss = number_of_conflicts(G, current_colors)
    temp = 100
    
    for i in range(n_iters):
        new_colors = tweak(current_colors, n_max_colors)
        new_loss = number_of_conflicts(G, new_colors)
        if new_loss < current_loss or np.random.randint(low=0, high=100) < temp:
            current_colors = new_colors
            current_loss = new_loss
        
        loss_history[i] = current_loss
        temp *= 0.99
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
