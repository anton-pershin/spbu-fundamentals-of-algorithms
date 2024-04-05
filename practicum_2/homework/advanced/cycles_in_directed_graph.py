import networkx as nx


TEST_GRAPH_FILES = [
    "graph_1_wo_cycles.edgelist",
    "graph_2_wo_cycles.edgelist",
    "graph_3_w_cycles_edgelist"
]


def has_cycles(g: nx.Graph) -> bool: 
    for node in list(g.nodes):
        if dfs_find(g, node, node):
            return True

    return False


def dfs_find(g:nx.Graph, start_node:str, target_node:str) -> bool:
    visited = set()
    stack = set()
    stack.add(start_node)

    while stack:
        node = stack.pop()

        if node in visited:
            continue
    
        visited.add(node)

        for neighbor in g.neighbors(node):
            if neighbor == target_node:
                return True

            if neighbor not in visited:
                stack.add(neighbor)

    return False


if __name__ == "__main__":
    for filename in TEST_GRAPH_FILES:
        # Load the graph
        G = nx.read_edgelist(filename, create_using=nx.DiGraph)
        # Output whether it has cycles
        print(f"Graph {filename} has cycles: {has_cycles(G)}")
