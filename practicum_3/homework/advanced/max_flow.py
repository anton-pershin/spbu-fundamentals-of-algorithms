from typing import Any

import networkx as nx

import numpy as np


def dfs(Graph: nx.Graph, start: Any, finish: Any, visited: dict, min_flow: Any):
    visited[start] = True
    if str(start) == str(finish):
        return min_flow
    for neighbor in Graph.out_edges(str(start), data=True):
        if not visited[neighbor[1]] and int(neighbor[2]["weight"][0]) > 0:
            flow = dfs(Graph, start=neighbor[1], finish=finish,
                       visited=visited, min_flow=min(min_flow, int(neighbor[2]["weight"][0])))
            if flow > 0:
                neighbor[2]["weight"][0] -= flow
                neighbor[2]["weight"][1] += flow
                return flow

    for neighbor in Graph.in_edges(str(start), data=True):
        if not visited[neighbor[0]] and int(neighbor[2]["weight"][1]) > 0:
            flow = dfs(Graph, start=neighbor[0], finish=finish,
                       visited=visited, min_flow=min(min_flow, int(neighbor[2]["weight"][1])))
            if flow > 0:
                neighbor[2]["weight"][0] += flow
                neighbor[2]["weight"][1] -= flow
                return flow

    return 0


def max_flow(Graph: nx.Graph, s: Any, t: Any) -> int:
    for i in Graph.edges(data=True):
        i[2]["weight"] = [i[2]["weight"], 0]

    value = 0

    while True:
        visited_nodes = {node: False for node in Graph.nodes()}
        flow = dfs(Graph, s, t, visited_nodes, np.inf)
        if flow > 0:
            value += flow
        else:
            break

    return value


if __name__ == "__main__":
    # Load the graph
    G = nx.read_edgelist("graph_1.edgelist", create_using=nx.DiGraph)
    val = max_flow(G, 0, 5)
    print(f"Maximum flow is {val}. Should be 23")
