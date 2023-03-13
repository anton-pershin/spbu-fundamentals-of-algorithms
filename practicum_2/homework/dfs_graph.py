from queue import LifoQueue
from typing import Any

import networkx as nx

from src.plotting import plot_graph


def visit(node: Any):
    print(f"Wow, it is {node} right here!")


def dfs_iterative(G: nx.Graph, node: Any):
    visited = {n: False for n in G}
    stack = LifoQueue()
    stack.put(node)

    # iterative dfs
    while not stack.empty():
        node = stack.get()
        if visited[node]:
            continue

        visited[node] = True
        visit(node)

        for neighbor in G.neighbors(node):
            stack.put(neighbor)


def topological_sort(G: nx.DiGraph, node: Any):
    visited = {n: False for n in G}
    graph_copy = G.copy()
    no_incoming_edges = [node for node in graph_copy if len(list(graph_copy.predecessors(node))) == 0]
    answer = []

    # iterative topological sort
    while no_incoming_edges:
        node = no_incoming_edges.pop()
        answer.append(node)

        visited[node] = True

        successors = list(graph_copy.successors(node))
        graph_copy.remove_node(node)
        for successor in successors:
            if len(list(graph_copy.predecessors(successor))) == 0 and not visited[successor]:
                no_incoming_edges.append(successor)

    # check if there are any remaining nodes in the graph
    if len(graph_copy) != 0:
        raise ValueError("The input graph has a cycle!")

    print(*answer)


if __name__ == "__main__":
    # Load and plot the graph
    G = nx.read_edgelist("graph_2.edgelist", create_using=nx.Graph)
    # plot_graph(G)

    print("Iterative DFS")
    print("-" * 32)
    dfs_iterative(G, node="0")
    print()

    G = nx.read_edgelist(
        "graph_2.edgelist", create_using=nx.DiGraph
    )
    plot_graph(G)
    print("Topological sort")
    print("-" * 32)
    topological_sort(G, node="0")
