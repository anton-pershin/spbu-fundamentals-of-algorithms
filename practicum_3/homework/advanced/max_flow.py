from typing import Any

import networkx as nx
import matplotlib.pyplot as plt

def dfs(g, s, t, parent) -> bool:
    was=set()
    stack=set()
    stack.add(s)
    while stack:
        node= stack.pop()

        if node in was:
            continue
        was.add(node)
        for neigh in g.neighbors(node):
            if neigh not in was:
                parent[neigh]= node
                stack.add(neigh)
    return t in was


def max_flow(G: nx.Graph, s: str, t: str):
    value: float = 0
    parent=dict()
    for node in G.nodes():
        parent[node]= None
    while dfs(G,s,t,parent):
        path_flow=float('inf')
        current_node=t
        while current_node != s:
            current_parent=parent[current_node]
            path_flow=min(path_flow,G[current_parent][current_node]['weight'])
            current_node=current_parent

        value+=path_flow

        current_node=t
        while current_node != s:
            current_parent=parent[current_node]
            G[current_parent][current_node]['weight']-=path_flow
            if (G[parent[current_node]][current_node]['weight']==0):
                G.remove_edge(current_parent,current_node)
            current_node = current_parent
    return value


if __name__ == "__main__":
    # Load the graph
    G = nx.read_edgelist("graph_1.edgelist", create_using=nx.DiGraph)
    val = max_flow(G, s="0", t="5")

    print(f"Maximum flow is {val}. Should be 23")

