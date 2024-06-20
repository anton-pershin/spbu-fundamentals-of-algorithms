
import os

import networkx as nx

TEST_GRAPH_FILES = [
    "graph_1_wo_cycles.edgelist",
    "graph_2_w_cycles.edgelist",
]

def has_cycles(g: nx.Graph) ->bool:
    visited = set()

    def dfs(node, parent):
        visited.add(node)
        for neighbor in g.neighbors(node):
            if neighbor not in visited:
                if dfs(neighbor, node):
                    return True
            elif neighbor != parent:
                return True
        return False

    for node in g.nodes():
        if node not in visited:
            if dfs(node, None):
                return True

    return False
if __name__ == "__main__":
    for filename in TEST_GRAPH_FILES:
        # Load the graph
        G = nx.read_edgelist(f"{filename}", create_using=nx.Graph)
        # Output whether it has cycles
        print(f"Graph {filename} has cycles: {has_cycles(G)}")
