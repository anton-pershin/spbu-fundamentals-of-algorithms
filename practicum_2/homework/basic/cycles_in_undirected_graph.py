import os

import networkx as nx


TEST_GRAPH_FILES = [
    "graph_1_wo_cycles.edgelist",
    "graph_2_w_cycles.edgelist",
]


def has_cycles(g: nx.Graph):
    def dfs(node, parent):
        visited.append(node)
        stack.append(node)

        for neighbor in g[node]:
            if neighbor == parent:
                continue

            if neighbor not in visited:
                if dfs(neighbor, node):
                    return True
            elif neighbor in stack:
                return True

        visited.remove(node)
        stack.pop()

        return False
    visited = []
    stack = []

    for node in g:
        if node not in visited:
            if dfs(node, None):
                return True

    return False


if __name__ == "__main__":
    for filename in TEST_GRAPH_FILES:
        # Load the graph
        G = nx.read_edgelist(
            os.path.join("practicum_2", "homework", filename), create_using=nx.Graph
        )
        # Output whether it has cycles
        print(f"Graph {filename} has cycles: {has_cycles(G)}")