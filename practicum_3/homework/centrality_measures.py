from typing import Any, Protocol
from itertools import combinations

import numpy as np
import networkx as nx

from src.plotting.graphs import plot_graph, plot_network_via_plotly
from src.common import AnyNxGraph

#вычисл протокола центральности
class CentralityMeasure(Protocol):
    name: str

    def __call__(self, G: AnyNxGraph) -> dict[Any, float]:
        ...

#вычисление центральности близости
def closeness_centrality(G: AnyNxGraph) -> dict[Any, float]:

    n = len(G.nodes) #общ кол узлов
    closeness = {}
    for node in G.nodes:
        path_lengths = nx.single_source_shortest_path_length(G, node)
        total_distance = sum(path_lengths.values())

        if total_distance == 0:
            closeness[node] = 0.0
        else:
            closeness[node] = (n - 1) / total_distance

    return closeness

#вычисление центральности посредничества
def betweenness_centrality(G: AnyNxGraph) -> dict[Any, float]:

    betweenness = {node: 0.0 for node in G.nodes}
    nodes = list(G.nodes)
    n = len(nodes)

    for s, t in combinations(nodes, 2):
        try:
            shortest_paths = list(nx.all_shortest_paths(G, s, t)) #все кратчайшие пути
            num_shortest_paths = len(shortest_paths) #кол-во кратчайших путей

            for v in G.nodes:
                if v not in (s, t): #v-промежуточная вершина?
                    num_shortest_paths_through_v = sum(1 for path in shortest_paths if v in path)
                    betweenness[v] += num_shortest_paths_through_v / num_shortest_paths if num_shortest_paths > 0 else 0

        #если нет путя s и t 
        except nx.NetworkXNoPath:
            pass
        
    for node in betweenness:
        betweenness[node] = betweenness[node] / ((n - 1) * (n - 2) / 2) if n > 2 else 0.0

    return betweenness

#вычисление собственных векторов
def eigenvector_centrality(G: AnyNxGraph) -> dict[Any, float]:

    try:
        eigenvector_centrality = nx.eigenvector_centrality(G)
        return eigenvector_centrality
    except nx.NetworkXError as e:
        print(f"Ошибка при вычислении eigenvector centrality: {e}")
        return None
    except nx.PowerIterationFailedConvergence as e:
        print(f"Итерационный процесс не сошелся: {e}")
        return None

#построение графика центральности
def plot_centrality_measure(G: AnyNxGraph, measure: CentralityMeasure) -> None:
    values = measure(G)
    if values is not None:
        plot_graph(G, node_weights=values, figsize=(14, 8), name=measure.name)
    else:
        print(f"Implement {measure.name}")


if __name__ == '__main__':
    #создаем грф
    graph = nx.karate_club_graph()

    closeness = closeness_centrality(graph)
    print("Closeness Centrality:", closeness)

    betweenness = betweenness_centrality(graph)
    print("Betweenness Centrality:", betweenness)

    eigenvector = eigenvector_centrality(graph)
    print("Eigenvector Centrality:", eigenvector)