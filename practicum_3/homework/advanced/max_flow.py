from typing import Any

import networkx as nx


def bfs(G: nx.Graph, s: Any, target: Any, parent: dict) -> bool:
    visited = set()
    visited.add(s)
    queue = [s]

    while queue:
        u = queue.pop(0)
        for neighbor, weight in G[u].items():
            if neighbor not in visited and weight['weight'] > 0:
                queue.append(neighbor)
                visited.add(neighbor)
                parent[neighbor] = u

    return target in visited


def max_flow(G: nx.Graph, s: Any, t: Any) -> int:
    value: int = 0
    parent = {}
    while bfs(G, s, t, parent):
        path_flow = float("inf")
        v = t
        while v != s:
            u = parent[v]
            path_flow = min(path_flow, G[u][v]['weight'])
            v = u
        value += path_flow
        v = t
        while v != s:
            u = parent[v]
            G[u][v]['weight'] -= path_flow
            if (v, u) not in G:
                G.add_edge(v, u, weight=0)
            G[v][u]['weight'] += path_flow
            v = u
    return value


if __name__ == "__main__":
    # Load the graph
    G = nx.read_edgelist("graph_1.edgelist", create_using=nx.DiGraph)

    val = max_flow(G, s='0', t='5')
    print(f"Maximum flow is {val}. Should be 23")
