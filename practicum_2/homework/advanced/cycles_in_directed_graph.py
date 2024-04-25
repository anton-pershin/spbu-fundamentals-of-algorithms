import os

import networkx as nx

TEST_GRAPH_FILES = [
    "graph_1_wo_cycles.edgelist",
    "graph_2_wo_cycles.edgelist",
    "graph_3_w_cycles.edgelist",
]

def has_cycles(g: nx.DiGraph):
    stack = set()
    visited = set()

    def dfs(node):
        if node in stack:
            return True
        if node in visited:
            return False
        stack.add(node)
        visited.add(node)
        for neighbor in g.neighbors(node):
            if dfs(neighbor)==True:
                return True
        stack.remove(node)
        return False

    for node in g.nodes:
        if dfs(node)==True:
            return True
        else:
            return False

if __name__ == "__main__":
    for filename in TEST_GRAPH_FILES:
        G = nx.read_edgelist( f"practicum_2/homework/advanced/{filename}", create_using=nx.DiGraph )
        print( f"Graph {filename} has cycles: {has_cycles(G)}" )
        # Load the graph
        G = nx.read_edgelist(
            os.path.join("practicum_2", "homework", filename), create_using=nx.DiGraph
        )
        # Output whether it has cycles
        print(f"Graph {filename} has cycles: {has_cycles(G)}")
