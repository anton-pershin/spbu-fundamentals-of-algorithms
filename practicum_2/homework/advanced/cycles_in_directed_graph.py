import os

import networkx as nx
import matplotlib.pyplot as plt  

TEST_GRAPH_FILES = [
    "graph_1_wo_cycles.edgelist",
    "graph_2_wo_cycles.edgelist",
    "graph_3_wo_cycles.edgelist",
    "graph_4_wo_cycles.edgelist"
]

def has_cycles(g: nx.DiGraph) -> bool:
    visited = set()
    rec_stack = set()

    def dfs(node):
        if node in rec_stack:
            return True
        if node in visited:
            return False

        visited.add(node)
        rec_stack.add(node)

        for neighbor in g.neighbors(node):
            if dfs(neighbor):
                return True

        rec_stack.remove(node)
        return False

    for node in g.nodes():
        if dfs(node):
            return True

    return False

if __name__ == "__main__":
    for filename in TEST_GRAPH_FILES:
        G = nx.read_edgelist(f"practicum_2/homework/advanced/{filename}", create_using=nx.DiGraph)
        print(f"Graph {filename} has cycles: {has_cycles(G)}")
        nx.draw(G)
        plt.show()