import numpy as np
from numpy.typing import NDArray
import networkx as nx

from src.plotting import plot_graph, plot_loss_history

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


def tweak(colors, n_max_colors, G):  ###вносим небольшое изменение в набор
    new_colors = colors.copy()

    random_index_start = np.random.randint(low=0, high=len(colors))  ###выбираем случайный нод
    node_color = colors[random_index_start]
    for i in nx.neighbors(G, random_index_start):  ###проходимся по соседям этого нода...
        neighbor_color = colors[i]
        while neighbor_color == node_color:
            neighbor_color = np.random.randint(low=0, high=n_max_colors)
        new_colors[i] = neighbor_color  ###и изменяем цвета соседей
    return new_colors


def decrease_temp(initial_temp, i, min_temp=0.01):  ###снижение температуры
    if initial_temp > min_temp:
        initial_temp = initial_temp / float(i + 1)
    return initial_temp


def transition_prob(old_res, new_res, temp, i):  ###вероятность смены
    P = 0
    if temp != 0:
        P = np.exp(-i / temp * (new_res - old_res) / old_res)
    return P


def solve_via_simulated_annealing(
        G: nx.Graph, n_max_colors: int, initial_colors: NDArrayInt, n_iters: int
):
    loss_history = np.zeros((n_iters,), dtype=np.int_)

    initial_temp = 100
    cur_colors = initial_colors
    temp = initial_temp
    for i in range(n_iters):

        loss_history[i] = number_of_conflicts(G, cur_colors)###запоминаем количество конфликтов для графика
        next_colors = tweak(cur_colors, n_max_colors, G)###создаём новый набор
        n_conflicts_new_colors = number_of_conflicts(G, next_colors)###узнаём количество конфликтов в новом наборе

        if number_of_conflicts(G,
                               cur_colors) > n_conflicts_new_colors:  # ##если количество конфликтов у нового набора
            # цветов меньше, чем у старого, то меняем
            cur_colors = next_colors

        else:
            probability = transition_prob(old_res=number_of_conflicts(G, cur_colors), new_res=n_conflicts_new_colors,
                                          temp=temp, i=i)
            rnd_num = np.random.rand()###если вероятность больше полученного числа, то всё равно меняем набор
            if probability > rnd_num:
                cur_colors = next_colors
                temp = decrease_temp(temp, i)
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
