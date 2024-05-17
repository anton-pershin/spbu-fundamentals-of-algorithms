import networkx as nx


TEST_GRAPH_FILES = [
    "graph_1_wo_cycles.edgelist",
    "graph_2_wo_cycles.edgelist",
    "graph_3_w_cycles_edgelist"
]


def cycles(node, g, visited, stack):
    visited.add(node)
    stack.add(node)
    for neighbour in g.neighbors(node):
        if neighbour not in visited:
            if cycles(neighbour, g, visited, stack):
                return True
        elif neighbour in stack:
            return True
    stack.remove(node)
    return False


def has_cycles(g: nx.DiGraph):
    visited = set()
    stack = set()
    for node in g.nodes():
        if node not in visited:
            if cycles(node, g, visited, stack):
                return True
    return False


if __name__ == "__main__":
    for filename in TEST_GRAPH_FILES:
        # Load the graph
        G = nx.read_edgelist(filename, create_using=nx.DiGraph)
        # Output whether it has cycles
        print(f"Graph {filename} has cycles: {has_cycles(G)}")