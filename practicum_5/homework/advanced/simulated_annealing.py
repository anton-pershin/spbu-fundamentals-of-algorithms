import numpy as np
from numpy.typing import NDArray
import networkx as nx

from src.plotting import plot_graph, plot_loss_history
import matplotlib.pyplot as plt

NDArrayInt = NDArray[np.int_]


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

def temperature_change(temperature, lamda=0.95):
     return temperature * lamda

def tweak(colors, n_max_colors):
    node_id = np.random.randint(0, len(colors))
    new_color = np.random.randint(0, n_max_colors)
    new_colors = colors.copy()
    new_colors[node_id] = new_color
    return new_colors

def solve_via_simulated_annealing(
    G: nx.Graph, n_max_colors: int, initial_colors: NDArrayInt, n_iters: int, temperature: int = 500,
):
    loss_history = np.zeros((n_iters,), dtype=np.int_)
    cur_colors = initial_colors.copy()
    chance_list = np.zeros((n_iters,), dtype=np.float64)
    temp_list = np.zeros((n_iters,), dtype=np.float64)
    for i in range(n_iters):
        next_colors = cur_colors.copy()
        loss_history[i] = number_of_conflicts(G, cur_colors)
        next_colors = tweak(cur_colors, n_max_colors)

        delta = (number_of_conflicts(G, cur_colors) - number_of_conflicts(G, next_colors))
        chance = np.exp(-1*abs(delta) / temperature)
        chance_list[i] = chance
        temp_list[i] = temperature
        if delta < 0 and chance > np.random.uniform(0, 1):
            print(f'Bylo = {number_of_conflicts(G,cur_colors)}, stalo - {number_of_conflicts(G,next_colors)}')
            cur_colors = next_colors    
        elif(delta > 0):
            cur_colors = next_colors
        temperature = temperature_change(temperature)


    x = np.linspace(0,500,500)
    ax = plt.plot(x,chance_list)
    


    return loss_history


if __name__ == "__main__":
    seed = 42
    np.random.seed(seed)
    G = nx.erdos_renyi_graph(n=100, p=0.05, seed=seed)
    #plot_graph(G)

    temperature = 500
    n_max_iters = 500
    n_max_colors = 3
    initial_colors = np.random.randint(low=0, high=n_max_colors - 1, size=len(G.nodes))

    loss_history = solve_via_simulated_annealing(
        G, n_max_colors, initial_colors, n_max_iters
    )
    print(loss_history[-1])
    plot_loss_history(loss_history)
    
