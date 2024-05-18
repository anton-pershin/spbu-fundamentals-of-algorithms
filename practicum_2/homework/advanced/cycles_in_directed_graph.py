import os
from typing import Any
import networkx as nx


TEST_GRAPH_FILES = [
    "graph_1_wo_cycles.edgelist",
    "graph_2_w_cycles.edgelist",
]

def dfs(g: nx.Graph, node: Any, visited: dict[Any]):
    if(visited[node] == 1):
        return True
    visited[node] = 1
    for i in nx.neighbors(g, node):
        if(dfs(g, i, visited)):
            return True
    visited[node] = 2
    return False
def has_cycles(g: nx.DiGraph):
    visited = {n: 0 for n in g}
    for n in g:
        if(visited[n] != 2):
            res = dfs(g, n, visited)
            if(res):
                return True
    return False

if __name__ == "__main__":
    for filename in TEST_GRAPH_FILES:
        # Load the graph
        G = nx.read_edgelist(
            os.path.join("practicum_2", "homework", filename), create_using=nx.DiGraph
        )
        # Output whether it has cycles
        print(f"Graph {filename} has cycles: {has_cycles(G)}")
