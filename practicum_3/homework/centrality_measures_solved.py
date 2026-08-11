
from typing import Any, Protocol
from itertools import combinations
import heapq

import numpy as np
import networkx as nx

from src.plotting.graphs import plot_graph, plot_network_via_plotly
from src.common import AnyNxGraph


class CentralityMeasure(Protocol):
    def __call__(self, G: AnyNxGraph) -> dict[Any, float]:
        ...


#  branch "... practicum_4"
#   -> "practicum_4/homework/dijkstra_solved.py"

def _dijkstra(G: AnyNxGraph, start_v: Any) -> tuple[dict, dict]:

    dist  = { start_v: 0.0 }
    num   = { start_v: 1   }

    pq    = [ (0.0, start_v) ]

    visited: set = set()

    while pq:

        d, u = heapq.heappop(pq)

        if u in visited: continue
        visited.add(u)

        for w in G.neighbors(u):

            weight   = float(G[u][w].get('weight', 1))
            new_dist = d + weight

            if w not in dist or new_dist < dist[w]:
                dist[w] = new_dist
                num[w]  = num[u]
                heapq.heappush(pq, (new_dist, w))

            elif new_dist == dist[w]:
                num[w] += num[u]

    return dist, num


# Близость (v)
#  = (число соседей) / (сумма кратчайших расстояний от v до других)

def closeness_centrality(G: AnyNxGraph) -> dict[Any, float]:

    nodes  = list(G.nodes())
    n      = len(nodes)
    result = {}

    for v in nodes:
        dist, _ = _dijkstra(G, v)
        total   = sum(dist.values())
        n_loc   = len(dist)

        if total > 0 and n > 1:
            # С поправкой для несвязных графов (Wasserman-Faust)
            result[v] = (n_loc - 1) / total * (n_loc - 1) / (n - 1)
        else:
            result[v] = 0.0

    return result


# Посредничество (v)
#  = сумма долей кратчайших путей между парами, в которых участвует v

def betweenness_centrality(G: AnyNxGraph) -> dict[Any, float]:

    nodes = list(G.nodes())
    n     = len(nodes)

    betweenness = { v: 0.0 for v in nodes }

    dists = {}
    nums  = {}
    
    for v in nodes:
        dists[v], nums[v] = _dijkstra(G, v)

    for s in nodes:
        for t in nodes:
            if s == t or t not in dists[s]:
                continue
            for v in nodes:
                if (v == s or v == t or 
                    v not in dists[s] or v not in dists[t]):
                    continue
                # Проверка, что v участвует в каком-то 
                #  кротчайшем пути (s,t)
                if dists[s][v] + dists[v][t] == dists[s][t]:
                    # += (способов добраться быстро через v) 
                    #     / (всего способов добраться быстро)
                    betweenness[v] += \
                        nums[s][v] * nums[v][t] / nums[s][t]

    if n > 2:
        # Нормировка как в networkx
        scale = 1.0 / ((n - 1) * (n - 2))
        for v in nodes:
            betweenness[v] *= scale

    return betweenness


# Влиятельность (v)
#  = 1/λ * (сумма влиятельностей соседей)

def eigenvector_centrality(G: AnyNxGraph) -> dict[Any, float]:

    # Ax = λx
    #
    # A – матрица смежности [VxV]
    # A[v, u] = weight (если есть ребро)
    # x – вектор влиятельностей [Vx1]
    # λ – число.
    #
    # x_0     = [1, 1, ..., 1]
    # x_{k+1} = A * x_k
    # x_{k+1} /= max

    nodes = list(G.nodes())
    A = nx.adjacency_matrix(G, nodelist=nodes).toarray().astype(float)

    # eigval[i]    == собственное число i
    # eigvec[:, i] == собственный вектор (столбец) i
    eigval, eigvec = np.linalg.eig(A)

    # Вектор при наибольшем вещественном собственном числе
    #  (Перрон-Фробениус)
    idx = np.argmax(eigval.real)
    x = eigvec[:, idx].real

    # Перрон-Фробениус гарантирует неотрицательность,
    #  но числовые погрешности могут дать минус
    if x.mean() < 0:
        x = -x

    x /= np.linalg.norm(x)

    return {nodes[i]: float(x[i]) for i in range(len(nodes))}


NX_MEASURE = {
    "closeness_centrality":   lambda G: nx.closeness_centrality(G, distance="weight"),
    "betweenness_centrality": lambda G: nx.betweenness_centrality(G, weight="weight"),
    "eigenvector_centrality": lambda G: nx.eigenvector_centrality(G, weight="weight"),
}


def plot_centrality_measure(G: AnyNxGraph, measure: CentralityMeasure) -> None:
    values = measure(G)
    if values is not None and measure.__name__ in NX_MEASURE:
        nx_vals = NX_MEASURE[measure.__name__](G)
        errors  = np.array([
            (values[v] - nx_vals[v]) / nx_vals[v]
            for v in G.nodes()
            if nx_vals[v] != 0
        ])
        print(f"{measure.__name__}: rel. errors = {np.round(errors, 3)}")

        zero_nx = {v: values[v] for v in G.nodes() if nx_vals[v] == 0}
        if zero_nx:
            print(f"{measure.__name__}: nx=0 nodes -> custom values: {zero_nx}")

    if values is not None:
        plot_graph(
            G,
            f"practicum_3/homework/plot/{measure.__name__}.png",
            node_weights=values,
            figsize=(14, 8),
            name=measure.__name__)
    else:
        print(f"Implement {measure.__name__}")


if __name__ == "__main__":

    # Zachary Karate Club (1977).

    # Социолог Уэйн Захари наблюдал за клубом карате из
    # 34 человек в течение двух лет.
    # Вес ребра между двумя участниками — количество социальных
    # контекстов вне тренировок, в которых они взаимодействовали.
    # Захари отслеживал 8 таких контекстов:
    # совместные посещения баров, академические занятия, общие тусовки и тд.
    # Вес 4 между узлами 0 и 1 означает, что эти двое пересекались
    # в 4 из 8 возможных контекстов.

    # То есть вес — мера силы дружеской связи, а не расстояние или стоимость.
    # Поэтому для мер центральности использовать веса как расстояния
    # неправильно по смыслу — большой вес означает более крепкую связь.

    G = nx.karate_club_graph()

    plot_centrality_measure(G, closeness_centrality)
    plot_centrality_measure(G, betweenness_centrality)
    plot_centrality_measure(G, eigenvector_centrality)
