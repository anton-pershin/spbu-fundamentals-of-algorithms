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

def tweak(G: nx.Graph, colors: NDArrayInt,maxColors : int) -> NDArrayInt:
    newColors = colors.copy()

    conflictNodes = []
    for u,v in G.edges:
        if colors[u] == colors[v]:
            conflictNodes.extend([u,v])

    if conflictNodes and np.random.random() < 0.8:
        node = np.random.choice(conflictNodes)
    else:
        node = np.random.randint(0,len(colors))

    currentColor = newColors[node]

    possibleColors = [c for c in range(maxColors) if c != currentColor]

    if len(possibleColors) > 0:
        newColors[node] = np.random.choice(possibleColors)

    return newColors;


def solve_via_simulated_annealing(
    G: nx.Graph, n_max_colors: int, initial_colors: NDArrayInt, n_iters: int
) -> NDArrayInt:
    loss_history = np.zeros((n_iters,), dtype=np.int_)
    
    currentColors = initial_colors.copy()
    currentConflicts = number_of_conflicts(G,currentColors)
    bestConflicts = currentConflicts

    T = 100.0

    for i in range(n_iters):
        loss_history[i] = bestConflicts
        if bestConflicts == 0:
            loss_history[i::] = 0
            break
        newColors = tweak(G,currentColors,n_max_colors)
        newConflicts = number_of_conflicts(G,newColors)
        d = newConflicts - currentConflicts

        if d <= 0 or np.random.rand() < np.exp(-d/T):
            currentColors = newColors
            currentConflicts = newConflicts
            bestConflicts = min(bestConflicts, currentConflicts)

        T *=0.9

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

