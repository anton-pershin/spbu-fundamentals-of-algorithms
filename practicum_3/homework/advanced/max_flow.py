from typing import Any

import networkx as nx


def residual_capacity(G, path):
    capacities = []
    for i in range(len(path) - 1):
        for j in range(i+1, len(path)):
            capacities.append(G[i][j]['weight'])
    return min(capacities)

def augment_flow(G, path, flow):
    for u, v in  zip(path, path[1:]):
        G[u][v]['weight'] += flow
        G[v][u]['weight'] -= flow

def find_augmenting_path(G, s, t):
    r = nx.shortest_path(G, source=s, target=t, weight='weight')
    print(r)
    return r

def max_flow(G: nx.DiGraph, s: Any, t: Any) -> int:
    ans = 0
    for u, v in G.edges():
        G[u][v]['weight'] = 0
    
    path = find_augmenting_path(G, s, t)
    while path:
        flow = residual_capacity(G, path)
        augment_flow(G, path, flow)
        path = find_augmenting_path(G, s, t)

    ans = sum(G[s][v]['weight'] for v in G.successors(s))
    return ans


if __name__ == "__main__":
    # Load the graph
    G = nx.read_edgelist("practicum_3/homework/advanced/graph_1.edgelist", create_using=nx.DiGraph)
    val = max_flow(G, s='0', t='5')
    print(f"Maximum flow is {val}. Should be 23")
