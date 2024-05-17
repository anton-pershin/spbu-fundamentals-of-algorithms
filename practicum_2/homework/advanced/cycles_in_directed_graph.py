import os

import networkx as nx


TEST_GRAPH_FILES = [
    "graph_1_wo_cycles.edgelist",
    "graph_2_wo_cycles.edgelist",
    "graph_3_w_cycles.edgelist"
]


def has_cycles(g: nx.DiGraph):
    def dfs_visit(node, visited, rec_stack):
        visited.add(node)
        rec_stack.add(node)
        for neighbor in g.neighbors(node):
            if neighbor not in visited:
                if dfs_visit(neighbor, visited, rec_stack):
                    return True
            elif neighbor in rec_stack:
                return True
        rec_stack.remove(node)
        return False
    visited = set()
    rec_stack = set()
    for node in g.nodes():
        if node not in visited:
            if dfs_visit(node, visited, rec_stack):
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
