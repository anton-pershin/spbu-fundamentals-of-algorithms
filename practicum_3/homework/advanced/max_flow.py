import copy
from typing import Any

# from src.plotting import plot_graph
import networkx as nx
import numpy as np


def edge_tuple_creator(array):
    result = []
    for i in range(len(array) - 1):
        result.append((array[i], array[i + 1]))
    return result


###Ford-Faulkerson Method
def max_flow(G: nx.DiGraph, s: Any, t: Any) -> int:
    value: int = 0
    G_tmp = copy.deepcopy(G)

    while True:
        try:
            path = nx.shortest_path(G_tmp, s, t)  ###перебираем все пути пока они не закончатся
        except nx.NetworkXNoPath:
            break

        print(f'path = {path}')

        path_edges = edge_tuple_creator(path)  ###создаём список с гранями
        min_flow_local = np.inf

        for i in range(len(path_edges)):  ###пробегаемся по всем граням из списка
            weight_list = nx.get_edge_attributes(G_tmp, "weight")  ###подтягиваем список весов
            if weight_list[path_edges[i]] < min_flow_local:
                min_flow_local = weight_list[path_edges[i]]  ###находим минимальный поток данного пути
        print(f'minimal flow = {min_flow_local}')
        value += min_flow_local  ###добавляем к общему максимальному потоку

        for j in range(len(path_edges)):
            edge_tuple = path_edges[j]
            G_tmp.edges[edge_tuple][
                "weight"] -= min_flow_local  # ##вычитаем полученный минимальный поток из веса каждого
            # использованного ребра

            if G_tmp.edges[edge_tuple]["weight"] == 0:
                G_tmp.remove_edge(edge_tuple[0], edge_tuple[1]) ###удаляем ребро при его нулевом весе


    return value


if __name__ == "__main__":
    # Load the graph
    G = nx.read_edgelist("graph_1.edgelist", create_using=nx.DiGraph)

    # plot_graph(G)
    val = max_flow(G, s='0', t='5')
    print(f"Maximum flow is {val}. Should be 23")
