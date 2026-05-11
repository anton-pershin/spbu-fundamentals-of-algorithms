import numpy as np
from numpy.typing import NDArray
import networkx as nx
import math

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

def tweaks(bestColors: NDArrayInt, n_max_colors: int) -> NDArrayInt:
    newColors = bestColors
    vertex = np.random.randint(0, len(newColors))
    neighColors = list()
    for neighbor in G.neighbors(vertex):
        neighColors.append(G.nodes[neighbor]["color"])
    colors = [color for color in range(n_max_colors) if color not in neighColors]
    if colors:
        newColors[vertex] = np.random.choice(colors)
    else:
        newColors[vertex] = np.random.randint(0, n_max_colors)
    return newColors

def toChange(temp: int, diff: int) -> bool:
    prob = math.exp((-diff) / temp) * 100
    if 0 <= np.random.randint(0, 100) <= prob:
        return True
    return False

def decreaseTemperature(start_temp, iteration, buff): 
    temp = start_temp / ((1 + iteration) * buff)
    return temp

def solve_via_simulated_annealing(
    G: nx.Graph, n_max_colors: int, initial_colors: NDArrayInt, n_iters: int
) -> NDArrayInt:
    loss_history = np.zeros((n_iters,), dtype=np.int_)
    bestColors = initial_colors
    bestConflicts = number_of_conflicts(G, initial_colors) 

    start_temp = 100 
    temp = start_temp
    for iteration in range(n_iters):
        buff = 1

        newColors = tweaks(bestColors, n_max_colors)
        newConflicts = number_of_conflicts(G, newColors)
        diff = abs(newConflicts - bestConflicts)
        
        if newConflicts <= bestConflicts:
            bestColors = newColors
            bestConflicts = newConflicts
            buff = 1.25

        else:
            if toChange(temp, diff) == True:
                bestColors = newColors
                bestConflicts = newConflicts
        loss_history[iteration] = bestConflicts
        temp = decreaseTemperature(start_temp, iteration, buff)

    return loss_history


if __name__ == "__main__":
    seed = 42
    np.random.seed(seed)
    G = nx.erdos_renyi_graph(n=100, p=0.05, seed=seed)
    #plot_graph(G)

    n_max_iters = 500
    n_max_colors = 3
    initial_colors = np.random.randint(low=0, high=n_max_colors - 1, size=len(G.nodes))

    loss_history = solve_via_simulated_annealing(
        G, n_max_colors, initial_colors, n_max_iters
    )
    print(np.min(loss_history))
    plot_loss_history(loss_history)
    print()
