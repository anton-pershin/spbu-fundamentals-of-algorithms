import networkx as nx
import copy

from typing import Any
from collections import deque

from src.plotting import plot_graph

# Поиск в ширину в остаточном графе
def bfs_residual(G: nx.DiGraph, s: int, t: int, parent: dict):
    visited = set()
    queue = deque()
    queue.append(s)
    visited.add(s)

    while queue:
        u = queue.popleft()
        for v in G.neighbors(u):
            if v not in visited and G[u][v]['weight'] > 0:
                queue.append(v)
                visited.add(v)
                parent[v] = u
                if v == t:
                    return True
    return False

# Алгоритм Форда-Фалкерсона для нахождения максимального потока
def max_flow(G: nx.DiGraph, s: int, t: int) -> int:
    parent = {}
    max_flow = 0

    # Поиск увеличивающего пути в остаточном графе
    while bfs_residual(G, s, t, parent):
        path_flow = float('inf')
        v = t
        # Нахождение пропускной способности увеличивающего пути
        while v != s:
            path_flow = min(path_flow, G[parent[v]][v]['weight'])
            v = parent[v]
        # Увеличение максимального потока и обновление остаточного графа
        max_flow += path_flow
        u = t
        while u != s:
            G[parent[u]][u]['weight'] -= path_flow
            u = parent[u]

    return max_flow


if __name__ == "__main__":
    G = nx.read_edgelist("practicum_3/homework/advanced/graph_1.edgelist", create_using=nx.DiGraph, nodetype=int)
    G_copy = copy.deepcopy(G)
    
    val = max_flow(G_copy, s=0, t=5)
    print(f"Maximum flow is {val}. Should be 23")
    plot_graph(G)
