from typing import Any, Protocol
from itertools import combinations

import numpy as np
import networkx as nx

from src.plotting.graphs import plot_graph, plot_network_via_plotly
from src.common import AnyNxGraph 
from collections import deque


class CentralityMeasure(Protocol):
    def __call__(self, G: AnyNxGraph) -> dict[Any, float]:
        ...

def closeness_centrality(G: AnyNxGraph) -> dict[Any, float]:
    data = {}
    for n in G:
        q = deque([n])
        dist = {n : 0}
        while q:
            v = q.popleft()
            for u in G.neighbors(v):
                if u not in dist:
                    dist[u] = dist[v] + 1
                    q.append(u)
        data[n] = (len(dist)-1)/sum(dist.values())
    return data;


def betweenness_centrality(G: AnyNxGraph) -> dict[Any, float]: 
    betweenness = {v: 0.0 for v in G.nodes}
    for start in G.nodes:
        dist = {start : 0}
        amount = {v: 0.0 for v in G.nodes}
        ancestor = {v: [] for v in G.nodes}
        q = deque([start])
        amount[start] = 1 

        backtrack = []

        while q:
            v = q.popleft()
            backtrack.append(v)
            for adj in G.neighbors(v):
                if adj not in dist:
                    dist[adj] = dist[v] + 1
                    q.append(adj)
                if dist[adj] == dist[v] + 1:
                    amount[adj] += amount[v]
                    ancestor[adj].append(v)
        
        delta = {v : 0 for v in G.nodes}
        while backtrack:
            v = backtrack.pop()
            for u in ancestor[v]:
                delta[u] += (amount[u] / amount[v]) * (1 + delta[v])

            if v != start:
                betweenness[v] += delta[v]

    n = len(G)
    scale = 1 / ((n-1) *  (n - 2) / 2 )
    for i in betweenness:
        betweenness[i] /= 2
        betweenness[i] *= scale

    return betweenness




def eigenvector_centrality(G: AnyNxGraph) -> dict[Any, float]: 

    ##########################
    ### PUT YOUR CODE HERE ###
    #########################

    pass


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
    #plot_centrality_measure(G, eigenvector_centrality)


