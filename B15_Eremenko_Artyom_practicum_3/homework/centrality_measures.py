from typing import Any, Protocol
from itertools import combinations

import numpy as np
import networkx as nx

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph

class CentralityMeasure(Protocol):
    def __call__(self, G: AnyNxGraph) -> dict[Any, float]:
        ...


def closeness_centrality(G: AnyNxGraph) -> dict[Any, float]:
    """
    Степень близости: обратно пропорциональна сумме расстояний до всех остальных узлов.
    Формула: C(u) = (n - 1) / sum(d(v, u))
    """
    nodes = list(G.nodes())
    n = len(nodes)
    closeness = {}

    for u in nodes:
        path_lengths = nx.single_source_shortest_path_length(G, u)
        sum_distances = sum(path_lengths.values())
        
        if sum_distances > 0 and n > 1:
            closeness[u] = (n - 1) / sum_distances
        else:
            closeness[u] = 0.0
            
    return closeness


def betweenness_centrality(G: AnyNxGraph) -> dict[Any, float]:
    """
    Степень посредничества: доля кратчайших путей, проходящих через узел.
    Для совпадения с nx используем алгоритм Брандеса или нормализацию.
    """
    betweenness = dict.fromkeys(G, 0.0)
    nodes = list(G.nodes())
    
    for s in nodes:
        S = []
        P = {v: [] for v in nodes}
        sigma = dict.fromkeys(nodes, 0.0)
        sigma[s] = 1.0
        d = dict.fromkeys(nodes, -1)
        d[s] = 0
        queue = [s]
        
        while queue:
            v = queue.pop(0)
            S.append(v)
            for w in G.neighbors(v):
                if d[w] < 0:
                    queue.append(w)
                    d[w] = d[v] + 1
                if d[w] == d[v] + 1:
                    sigma[w] += sigma[v]
                    P[w].append(v)
        
        delta = dict.fromkeys(nodes, 0.0)
        while S:
            w = S.pop()
            for v in P[w]:
                delta[v] += (sigma[v] / sigma[w]) * (1.0 + delta[w])
            if w != s:
                betweenness[w] += delta[w]

    n = len(nodes)
    scale = 1.0 / ((n - 1) * (n - 2)) if n > 2 else 1.0
    for v in betweenness:
        betweenness[v] *= scale
        
    return betweenness


def eigenvector_centrality(G: AnyNxGraph, max_iter=100, tol=1.0e-6) -> dict[Any, float]:
    nodes = list(G.nodes())
    x = {node: 1.0 / len(nodes) for node in nodes}
    
    for _ in range(max_iter):
        x_last = x.copy()
        for u in nodes:
            total = 0
            for v in G.neighbors(u):
                total += x_last[v]
            x[u] = total
            
        norm = np.sqrt(sum(v**2 for v in x.values()))
        if norm == 0:
            return x
        for u in x:
            x[u] /= norm
            
        if sum(abs(x[u] - x_last[u]) for u in x) < tol:
            break
            
    return x


def plot_centrality_measure(G: AnyNxGraph, measure: CentralityMeasure) -> None:
    values = measure(G)
    if values is not None:
        try:
            plot_graph(G, node_weights=values, figsize=(14, 8), name=measure.__name__)
        except:
            print(f"Computed {measure.__name__}: {list(values.items())[:3]}...")
    else:
        print(f"Implement {measure.__name__}")


if __name__ == "__main__":
    G = nx.karate_club_graph()

    # my_closeness = closeness_centrality(G)
    # nx_closeness = nx.closeness_centrality(G)
    
    # is_closeness_correct = all(np.isclose(my_closeness[n], nx_closeness[n]) for n in G.nodes())
    # print(f"Closeness Centrality match: {is_closeness_correct}")


    # my_betweenness = betweenness_centrality(G)
    # nx_betweenness = nx.betweenness_centrality(G, normalized=True)
    
    # is_betweenness_correct = all(np.isclose(my_betweenness[n], nx_betweenness[n]) for n in G.nodes())
    # print(f"Betweenness Centrality match: {is_betweenness_correct}")


    # my_eigen = eigenvector_centrality(G)
    # nx_eigen = nx.eigenvector_centrality(G, max_iter=100)
    
    # is_eigen_correct = all(np.isclose(my_eigen[n], nx_eigen[n], atol=1e-05) for n in G.nodes())
    # print(f"Eigenvector Centrality match: {is_eigen_correct}")
    
    print("Running centrality measures...")
    plot_centrality_measure(G, closeness_centrality)
    plot_centrality_measure(G, betweenness_centrality)
    plot_centrality_measure(G, eigenvector_centrality)
    print("Done!")