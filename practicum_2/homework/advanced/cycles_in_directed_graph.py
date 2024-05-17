import os

import networkx as nx
from typing import Any
from src.plotting import plot_graph

TEST_GRAPH_FILES = [
    "graph_1_wo_cycles.edgelist",
    "graph_2_wo_cycles.edgelist",
    "graph_3_w_cycles_edgelist"
]

FLAG = False

def neighbours_for_DiGraph(G: nx.DiGraph, node: Any):
    arr = []
    for i in G.edges:
        if (i[0] == node):
            arr.append(i[1])
    return arr

def has_cycles(G: nx.DiGraph, node: Any, visited: dict[Any], ancestor=-1) -> None:
    global FLAG
    if (visited[node] == False and FLAG == False):
        visited[node] = True
        arr = neighbours_for_DiGraph(G, node)
        for i in arr:
            if(i != ancestor): # we check if comliper will go to the previous node
                if(visited[i] == True): # if we made a circle and meet TRUE node
                    FLAG = True
                else:
                    has_cycles(G, i, visited, node)
                    visited[i] = False


if __name__ == "__main__":
    a = "practicum_2/homework/advanced/graph_1_wo_cycles.edgelist"
    b = "practicum_2/homework/advanced/graph_2_wo_cycles.edgelist"
    c = "practicum_2/homework/advanced/graph_3_w_cycles_edgelist"
    tmp = 0
    for filename in TEST_GRAPH_FILES:
        if (tmp == 0):
            i = a
            tmp+=1
        elif (tmp == 1):
            i = b
            tmp+=1
        else:
            i = c
        G = nx.read_edgelist(i, create_using=nx.DiGraph)
        plot_graph(G)
        visited = {n: False for n in G}
        print(f"Graph {filename}: " , end = '')
        has_cycles(G, node="0", visited=visited)
        if (FLAG == True):
            print("there is a cycle!")
        else:
            print("no cycle here!")

