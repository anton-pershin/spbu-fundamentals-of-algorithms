from typing import Any

import networkx as nx
import queue
import matplotlib.pyplot as plt
from src.plotting import plot_graph
from copy import deepcopy

def dfs(G: nx.Graph, s: Any, parent: dict[Any], t: Any, c: Any) -> bool:
    t = str(t)
    s = str(s)
    visited = {n: 0 for n in G}
    q = queue.LifoQueue()

    q.put(s)
    while not q.empty():
        v = q.get()
        if v == t:
            return True
        visited[v] = True

        for neigh in G.neighbors(v):
            if not visited[neigh] and G[v][neigh]['weight'] >= c:
                parent[neigh] = v        
                q.put(neigh)
    return False
    


def max_flow(G: nx.Graph, s: Any, t: Any) -> int:
    s = str(s)
    t = str(t)
    value: int = 0
    
    c = 100 # Some threshold value for weight of edge 

    parents = {i : -1 for i in G.nodes}

    min_flow = 1000

    while c > 0:
        if not dfs(G, s, parents, t, c):
            c //= 2
            if c == 0:
                break
        else:
            v = t
            while parents[v] != -1:
                min_flow = min(min_flow, G[parents[v]][v]['weight'])
                v = parents[v]
            value += min_flow
            v = t
            while parents[v] != -1:
                G[v][parents[v]]['weight'] += min_flow
                G[parents[v]][v]['weight'] -= min_flow
                v = parents[v]
            min_flow = 1000
            parents = {i : -1 for i in G.nodes}

    return value


if __name__ == "__main__":
    # Load the graph
    G = nx.read_edgelist("practicum_3/homework/advanced/graph_1.edgelist", create_using=nx.DiGraph)
    G_copy = deepcopy(G)
    
    edges = []
    for u, v in G.edges():
        edges.append((v, u, 0))
    G_copy.add_weighted_edges_from(edges)

    visited = {int(n): 0 for n in G.nodes}
    
    val = max_flow(G_copy, s = 0, t = 5)

    print(f"Maximum flow is {val}. Should be 23")