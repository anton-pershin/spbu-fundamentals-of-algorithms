from typing import Any, Protocol
from itertools import combinations
import numpy as np
import networkx as nx

from src.plotting.graphs import plot_graph, plot_network_via_plotly
from src.common import AnyNxGraph 

def closeness_centrality(G: AnyNxGraph) -> dict[Any, float]:
    res = {}
    n = len(G)
    
    for v in G:
        if G.is_directed():
            path = nx.shortest_path_length(G, target=v)
        else:
            path = nx.shortest_path_length(G, v)

        dist = sum(path.values())
        if dist > 0:
            res[v] = (n - 1) * (1 / dist)
        else:
            res[v] = 0

    return res


def betweenness_centrality(G: AnyNxGraph) -> dict[Any, float]: 
    res = {}
    for v in G:
        res[v] = 0.0
    num = len(G)
    
    for s in G:
        for t in G:
            if s != t:
                all_paths = list(nx.all_shortest_paths(G, s, t))
                n = len(all_paths)
                for path in all_paths:
                    for v in path[1: -1]:
                        res[v] += 1 / n

    norm = (num - 1) * (num - 2)
    for x in res:
        res[x] /= norm
    return res


def eigenvector_centrality(G: AnyNxGraph) -> dict[Any, float]: 
    c = {}
    for v in G:
        c[v] = 1.0

    A = nx.to_numpy_array(G)
    eigenvalues = np.linalg.eigvals(A)
    l = max(abs(eigenvalues))

    for i in range(100):
        c1 = {}
        for v in G:
            if G.is_directed():
                s = sum(c[u] for u in G.predecessors(v))
            else:
                s = sum(c[u] for u in G.neighbors(v))

            c1[v] = (1 / l) * s
            norm = sum(x**2 for x in c1.values())**0.5
        for v in c1:
            c1[v] = c1[v] / norm
        c = c1
    return c

G = nx.karate_club_graph()
    
my_closeness = closeness_centrality(G)
nx_closeness = nx.closeness_centrality(G)
print("Closeness Centrality:")
for node in G.nodes():
    print(node, my_closeness[node], nx_closeness[node])


my_betweenness = betweenness_centrality(G)
nx_betweenness = nx.betweenness_centrality(G)
print("\nBetweenness Centrality:")
for node in G.nodes():
    print(node, my_betweenness[node], nx_betweenness[node])

my_eigenvector = eigenvector_centrality(G)
nx_eigenvector = nx.eigenvector_centrality_numpy(G)
print("\nEigenvector Centrality:")
for node in G.nodes():
    print(node, my_eigenvector[node], nx_eigenvector[node])

DG = nx.DiGraph()
DG.add_edges_from([
    (0, 1), (1, 2), (2, 0),
    (2, 3), (3, 4), (4, 2),
    (1, 3), (4, 0)
])

my_closeness = closeness_centrality(DG)
nx_closeness = nx.closeness_centrality(DG)
print("Closeness Centrality (Directed):")
for node in DG.nodes():
    print(node, my_closeness[node], nx_closeness[node])


my_betweenness = betweenness_centrality(DG)
nx_betweenness = nx.betweenness_centrality(DG)
print("\nBetweenness Centrality (Directed):")
for node in DG.nodes():
    print(node, my_betweenness[node], nx_betweenness[node])


my_eigenvector = eigenvector_centrality(DG)
nx_eigenvector = nx.eigenvector_centrality_numpy(DG)
print("\nEigenvector Centrality (Directed):")
for node in DG.nodes():
    print(node, my_eigenvector[node], nx_eigenvector[node])