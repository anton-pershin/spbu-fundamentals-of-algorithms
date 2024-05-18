from typing import Any

import networkx as nx

def bfs(G, s, t, parent):
    visited = [False] * G.number_of_nodes()
    queue = []
    queue.append(s)
    visited[s] = True
    
    while queue:
        u = queue.pop(0)
        for v, r in enumerate(G[u]):
            if visited[v] == False and r > 0:
                queue.append(v)
                visited[v] = True
                parent[v] = u
    return True if visited[t] else False

def max_flow(G: nx.G, s: Any, t: Any):

    max_flow = 0
    parent = [-1] * G.number_of_nodes()
    while bfs(G, s, t, parent):
        path_flow = float('inf')
        s = t
        while s != s:
            path_flow = min(path_flow, G[parent[s]][s])
            s = parent[s]
        
        max_flow += path_flow
        v = t
        while v != s:
            u = parent[v]
            G[u][v] -= path_flow
            G[v][u] += path_flow
            v = parent[v]
    return max_flow


if __name__ == "__main__":
    # Load the graph
    G = nx.read_edgelist("practicum_3/homework/advanced/graph_1.edgelist", create_using=nx.DiGraph)
    
    val = max_flow(G, s=0, t=5)
    print(f"Maximum flow is {val}. Should be 23")
