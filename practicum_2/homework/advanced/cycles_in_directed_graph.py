import networkx as nx


TEST_GRAPH_FILES = [
    "graph_1_wo_cycles.edgelist",
    "graph_2_wo_cycles.edgelist",
    "graph_3_w_cycles_edgelist",
]

"""
def has_cycles(g: nx.DiGraph) -> bool:
    try:
        nx.find_cycle(g, orientation="original")
        return True
    except nx.NetworkXNoCycle:
        return False
"""

"""
def has_cycles(g: nx.Graph) -> bool:
    return len(list(nx.simple_cycles(g))) > 0
"""

def has_cycles(g: nx.DiGraph):
    visited = set()
    stack = set()

    def dfs(node):
        visited.add(node)
        stack.add(node)
        for neighbor in g.neighbors(node):
            if neighbor not in visited:
                if dfs(neighbor):
                    return True
            elif neighbor in stack:
                return True
        stack.remove(node)
        return False

    for node in g.nodes:
        if node not in visited:
            if dfs(node):
                return True
    return False

if __name__ == "__main__":
    for filename in TEST_GRAPH_FILES:
        # Load the graph
        G = nx.read_edgelist(f"practicum_2/homework/advanced/{filename}", create_using=nx.DiGraph)
        # Output whether it has cycles
        print(f"Graph {filename} has cycles: {has_cycles(G)}")