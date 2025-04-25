from typing import Any, Protocol
from itertools import combinations
from collections import deque

import numpy as np
import networkx as nx
from networkx.classes import is_directed

from src.plotting.graphs import plot_graph, plot_network_via_plotly
from src.common import AnyNxGraph 


class CentralityMeasure(Protocol):
    def __call__(self, G: AnyNxGraph) -> dict[Any, float]:
        ...


def closeness_centrality(G: AnyNxGraph) -> dict[Any, float]:
    result = {}
    n = len(G)

    for node in G.nodes():
        # {узел: длина кратчайшего пути}
        distances = nx.shortest_path_length(G, source=node)

        # сумма расстояний кроме нулевого расстояния до самого себя
        sum_dist = sum(d for target, d in distances.items() if target != node)

        reachable = len(distances) - 1 # число достижимых узлов

        # случай если узел изолирован
        if sum_dist > 0:
            result[node] = reachable / sum_dist
        else:
            result[node] = 0.0

    return result

def betweenness_centrality(G: AnyNxGraph) -> dict[Any, float]:
    nodes = list(G.nodes())
    betweenness = {node: 0.0 for node in nodes}

    # Алгоритм Брандеса

    # Для каждой вершины start считаем вклад в betweenness
    for start in nodes:
        # список предшественников
        predecessors = {n: [] for n in nodes}
        # расстояние (число ребер)
        distance = {n: -1 for n in nodes}
        distance[start] = 0
        # число кратчайших путей
        sigma = {n: 0 for n in nodes}
        sigma[start] = 1.0

        stack = [] # стек порядка для обратного накопления
        queue = deque([start]) # очередь для BFS

        # BFS
        while queue:
            current = queue.popleft()
            stack.append(current)

            for neighbor in G.neighbors(current):
                # если не посещен, добавляем расстояние и обновляем очередь
                if distance[neighbor] < 0:
                    distance[neighbor] = distance[current] + 1
                    queue.append(neighbor)
                # если обнаружен кратчайший путь, обновляем счетчик sigma и предшественников
                if distance[neighbor] == distance[current] + 1:
                    sigma[neighbor] += sigma[current]
                    predecessors[neighbor].append(current)

        # Копим зависимости

        # суммарная зависимость всех пар узлов проходящих через вершины
        delta = {n: 0.0 for n in nodes}
        # Проходим узлы в обратном порядке стека
        while stack:
            neighbor = stack.pop()
            for current in predecessors[neighbor]:
                # формула по Брандесу
                delta[current] += (sigma[current] / sigma[neighbor]) * (1 + delta[neighbor])

            if neighbor != start:
                betweenness[neighbor] += delta[neighbor]

    # Нормализация
    n = len(nodes)
    for current in betweenness:
        betweenness[current] *= 1 / ((n-1)*(n-2))

    return betweenness

def eigenvector_centrality(G: AnyNxGraph) -> dict[Any, float]:
    nodes = list(G.nodes())
    n = len(nodes)
    idx = {node: i for i, node in enumerate(nodes)}

    # Строим матрицу смежности
    A = np.zeros((n, n), dtype=float)
    for u, v in G.edges():
        i, j = idx[u], idx[v]
        A[i,j] = 1.0
        if not G.is_directed():
            A[j,i] = 1.0

    # Вычисляем собственные значения и собственные векторы
    eigenvalues, eigenvectors = np.linalg.eig(A)

    # Ищем индекс максимального по модулю собственного значения
    principal = np.argmax(np.abs(eigenvalues))
    principal_vector = np.real(eigenvectors[:, principal])

    # Нормируем вектор
    principal_vector /= np.linalg.norm(principal_vector)

    # Возвращаем значения по узлам
    return {nodes[i]: float(principal_vector[i]) for i in range(n)}

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

    # Степень близости | совпадают
    # print(nx.closeness_centrality(G))
    # print(closeness_centrality(G))

    # Степень посредничества | совпадают
    # print(nx.betweenness_centrality(G))
    # print(betweenness_centrality(G))

    # Степень влиятельности | совпадают
    # print(nx.eigenvector_centrality(G))
    # print(eigenvector_centrality(G))