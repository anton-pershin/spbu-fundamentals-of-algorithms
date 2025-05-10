from typing import Any, Protocol
from itertools import combinations

import numpy as np
import networkx as nx

from src.plotting.graphs import plot_graph, plot_network_via_plotly
from src.common import AnyNxGraph 


class CentralityMeasure(Protocol):
    def __call__(self, G: AnyNxGraph) -> dict[Any, float]:
        ...


def closeness_centrality(G: AnyNxGraph) -> dict[Any, float]:
    closeness = {}
    for node in G.nodes():
        # Находим кратчайшие расстояния от узла до всех остальных узлов
        lengths = bfs_shortest_path_lengths(G, node)
        # Вычисляем близость как обратное среднее расстояние
        total_length = sum(lengths.values())
        if len(lengths) > 1:
            closeness[node] = (len(lengths) - 1) / total_length
        else:
            closeness[node] = 0.0
    return closeness


def betweenness_centrality(G: AnyNxGraph) -> dict[Any, float]: 
    betweenness = defaultdict(float)
    
    for s in G.nodes():
        for t in G.nodes():
            if s != t:
                # Находим все кратчайшие пути от s до t
                paths = all_shortest_paths(G, s, t)
                num_paths = len(paths)
                
                for path in paths:
                    for node in path[1:-1]:  # Исключаем начальный и конечный узлы
                        betweenness[node] += 1 / num_paths
    
    return betweenness


def eigenvector_centrality(G: AnyNxGraph) -> dict[Any, float]: 
    n_nodes = len(G.nodes())
    eigenvector = {node: 1.0 for node in G.nodes()}  # Начальное значение

    for _ in range(100):  # Итерации для сходимости
        new_eigenvector = {}
        for node in G.nodes():
            new_eigenvector[node] = sum(eigenvector[neighbor] for neighbor in G.neighbors(node))
        
        # Нормируем вектор
        norm_factor = np.linalg.norm(list(new_eigenvector.values()))
        new_eigenvector = {node: value / norm_factor for node, value in new_eigenvector.items()}
        
        eigenvector = new_eigenvector

    return eigenvector


def plot_centrality_measure(G: AnyNxGraph, measure: CentralityMeasure) -> None:
    values = measure(G)
    if values is not None:
        plot_graph(G, node_weights=values, figsize=(14, 8), name=measure.__name__)
    else:
        print(f"Implement {measure.__name__}")


if __name__ == "__main__":
    G = nx.karate_club_graph()
    
    plot_centrality_measure(G, closeness_centrality)
    plot_centrality_measure(G, betweenness_centrality)
    plot_centrality_measure(G, eigenvector_centrality)

