import os

import networkx as nx
import queue
from typing import Any
import networkx as nx
from src.plotting import plot_graph

TEST_GRAPH_FILES = [
    "graph_1_wo_cycles.edgelist",
    "graph_2_w_cycles.edgelist",
]


def dfs(G: nx.Graph, node: Any, parent: Any, visited: dict[Any]):
    if(visited[node] == 1):
        return True
    visited[node] = 1
    for i in nx.neighbors(G, node):
        if(i != parent):
            if(dfs(G, i, node, visited)):
                return True
    visited[node] = 2
    return False
    
def has_cycles(G: nx.Graph):
    visited = {n: 0 for n in G}
    for n in G:
        if(visited[n] != 2):
            res = dfs(G, n, n, visited) 
            if(res):
                return True
    return False
if __name__ == "__main__":
    g = nx.Graph()
    for filename in TEST_GRAPH_FILES:
        # Load the graph
<<<<<<< HEAD
        G = nx.read_edgelist("practicum_2/homework/basic/" + filename, create_using=nx.Graph)
        plot_graph(G)        
       # Output whether it has cycles
=======
        G = nx.read_edgelist(
            os.path.join("practicum_2", "homework", filename), create_using=nx.Graph
        )
        # Output whether it has cycles
>>>>>>> b567133b1f1679751f3681ee2b532c0f5acfa386
        print(f"Graph {filename} has cycles: {has_cycles(G)}")
