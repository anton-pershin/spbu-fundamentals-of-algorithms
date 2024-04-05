import queue
from typing import Any

import networkx as nx

from src.plotting import plot_graph

def visit(node: Any):
    print(f"Wow, it is {node} right here!")

def neighbours(G: nx.Graph, node: Any):
    arr = []
    for i in G.edges:
        if (node in i):
            if (i[0] != node):
                arr.append(i[0])
            else:
                arr.append(i[1])
    return arr

def dfs_recursive(G: nx.Graph, node: Any, visited: dict[Any]) -> None:
    if (visited[node] == False):
        visited[node] = True
        visit(node)
        arr = neighbours(G, node)
        for i in arr:
            dfs_recursive(G, i, visited)

def dfs_iterative(G: nx.Graph, node: Any) -> None:
    #visit(node)
    stack = [node]
    visited = {n: False for n in G}
    cur_node = node
    while (len(stack) != 0):
        cur_node = stack[-1]
        stack.pop(-1)
        if (visited[cur_node] == False):
            visit(cur_node)
            visited[cur_node] = True
            
        arr_neighbours = neighbours(G, cur_node) 
           
        for i in range(len(arr_neighbours)):
            
            if (visited[arr_neighbours[i]] == False):
                stack.append(arr_neighbours[i])
            
def dfs_recursive_postorder(G: nx.DiGraph, node: Any, visited: dict[Any]) -> None:
    if (visited[node] == False):
        visited[node] = True
        arr = neighbours(G, node)
        for i in arr:
            dfs_recursive_postorder(G, i, visited)
        visit(node)

if __name__ == "__main__":
    # Load and plot the graph
    G = nx.read_edgelist("practicum_2/graph_2.edgelist", create_using=nx.Graph)
    #plot_graph(G)

    # 1. Recursive DFS. Trivial to implement, but it does not scale on large graphs
    # In the debug mode, look at the call stack
    print("Recursive DFS")
    print("-" * 32)
    visited = {n: False for n in G}
    dfs_recursive(G, node="0", visited=visited)
    print()


    
    #arr = neighbours(G, node="5")
   # print(arr)
    # 2. Iterative DFS. Makes use of LIFO/stack data structure, does scale on large graphs
    print("Iterative DFS")
    print("-" * 32)
    #dfs_iterative(G, node="0")
    print()

    # 3. Postorder recursive DFS for topological sort
    # If a directed graph represent tasks to be done, the topological sort tells
    # us what the task order should be, i.e. scheduling
    # Postorder DFS outputs the reversed order!
    G = nx.read_edgelist("practicum_2/graph_2.edgelist", create_using=nx.DiGraph)
    #plot_graph(G)
    print("Postorder iterative DFS")
    print("-" * 32)
    visited = {n: False for n in G}
    dfs_recursive_postorder(G, node="0", visited=visited)
