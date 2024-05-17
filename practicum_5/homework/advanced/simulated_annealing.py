from typing import Protocol
import numpy as np
from numpy.typing import NDArray
import networkx as nx

from src.plotting import plot_graph, plot_loss_history

NDArrayInt = NDArray[np.int_]

average_mistakes = []

class GraphColoringSolver(Protocol):
    def __call__(
        G: nx.Graph, n_max_colors: int, initial_colors: NDArrayInt, n_iters: int
    ) -> NDArrayInt:
        pass

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

def temperature_changing(temperature) -> int:
    num = 0.898011
    temperature = temperature * num
# 0.9 
    return temperature


''' 
## The idea of this func is that we check amount of neighbours and if  ##
## it's big enough, than we color them into one colour different from  ##
## the one that original node has                                      ##
## Else we just colour our original node into different colour         ##
'''
def new_new_new_tweaks1(G: nx.Graph, colors, n_max_colors): 
    new_colors = colors.copy()
    rand_node = np.random.randint(low=0, high=len(G.nodes))
    color_of_node_we_check = colors[rand_node]
    rand_color = np.random.randint(0, n_max_colors)
    
    while (color_of_node_we_check == rand_color):
        rand_color = np.random.randint(0, n_max_colors)
        
    if len(list(G.neighbors(rand_node))) >= 8:
        for i in G.neighbors(rand_node):
            new_colors[i] = rand_color
    else:
        new_colors[rand_node] = rand_color
            
    return new_colors

def new_new_new_tweaks(G: nx.Graph, colors, n_max_colors):
    new_colors = colors.copy()
    
    num = np.random.uniform(0, 1)
    
    rand_node = np.random.randint(low=0, high=len(G.nodes))
    color_of_node_we_check = colors[rand_node]
    rand_color = np.random.randint(0, n_max_colors)
    
    while (color_of_node_we_check == rand_color):
        rand_color = np.random.randint(0, n_max_colors)
        
    if len(list(G.neighbors(rand_node))) >= 8:
        for i in G.neighbors(rand_node):
            new_colors[i] = rand_color
    else:
        new_colors[rand_node] = rand_color
            
    return new_colors

def solve_via_simulated_annealing_restarts(
    solver: GraphColoringSolver, 
    G: nx.Graph,
    n_max_colors: int, 
    initial_colors: NDArrayInt,
    n_iters: int,
    n_restarts: int
)-> NDArrayInt:
    loss_history = np.zeros((n_restarts, n_iters), dtype=np.int_)
    for i in range(n_restarts):
        print(f"Restart #{i + 1}")
        initial_colors = np.random.randint(0, n_max_colors - 1, len(G.nodes))
        set_colors(G, initial_colors)  
        loss_history_per_run = solver(G, n_max_colors, initial_colors, n_max_iters)
        loss_history[i, :] = loss_history_per_run
    return loss_history
    

def solve_via_simulated_annealing(
    G: nx.Graph,
    n_max_colors: int, 
    initial_colors: NDArrayInt,
    n_iters: int,
):
    global average_mistakes
    loss_history = np.zeros((n_iters,), dtype=np.int_)
    cur_colors = initial_colors.copy()
    next_colors = initial_colors.copy()
    
    counter = 0
    temperature = 1
    arr_of_loss_history = []
    
    probability_history = np.zeros((n_iters,), dtype=np.float64)
    temperature_history = np.zeros((n_iters,), dtype=np.float64)
    
    for i in range(n_iters):
        if(temperature >= 0):
            loss_history[i] = number_of_conflicts(G, cur_colors)
            arr_of_loss_history.append(loss_history[i])
            next_colors = new_new_new_tweaks(G, cur_colors, n_max_colors)

            cur_confl = number_of_conflicts(G, cur_colors)
            new_confl = number_of_conflicts(G, next_colors)
            
            delta_energy = cur_confl - new_confl
            probability = np.exp((abs(delta_energy) * (-1)) / temperature)
            
            probability_history[counter] = probability

            num = np.random.uniform(0, 1)
            if (delta_energy <= 0 and num <= probability):
                cur_colors = next_colors
            elif delta_energy > 0:
                cur_colors = next_colors
            temperature = temperature_changing(temperature=temperature)
            temperature_history[counter] = temperature
            counter+=1
        
    average_mistakes.append(min(arr_of_loss_history))
    #plot_loss_history(probability_history)
    #plot_loss_history(temperature_history) 
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
    
    '''
    n_restarts = 20
    loss_history = solve_via_simulated_annealing_restarts(
        solve_via_simulated_annealing,
        G,
        n_max_colors,
        initial_colors,
        n_max_iters,
        n_restarts,
    )
    

    print()
    print(f"Were made {n_restarts} restarts")
    print("Average amount of mistakes:", sum(average_mistakes) / n_restarts)
    print("Minimum mistakes:", min(average_mistakes))
    '''
    plot_loss_history(loss_history)
   
    '''
    print("Would you like to print a graph? y/n")
    
    answer = input()
    if (answer == "yes")  or answer ==  "y" or answer ==  "Y":
        plot_loss_history(loss_history)
    '''
