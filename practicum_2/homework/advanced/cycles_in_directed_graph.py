import networkx as nx


TEST_GRAPH_FILES = [
    "graph_1_wo_cycles.edgelist",
    "graph_2_wo_cycles.edgelist",
    "graph_3_wo_cycles.edgelist",
]


def has_cycles(g: nx.DiGraph):
    visited = {node: False for node in g.nodes()}
    
    for node in g.nodes():
        if not visited[node]:
            if dfs_cycle_check(g, node, visited, None):
                return "yes"

    return "no"

def dfs_cycle_check(g, node, visited, parent):
    visited[node] = True

    for neighbor in g[node]:
        if not visited[neighbor]:
            if dfs_cycle_check(g, neighbor, visited, node):
                return True
        elif neighbor != parent:
            return True

    return False


if __name__ == "__main__":
    for filename in TEST_GRAPH_FILES:
        # Load the graph
        G = nx.read_edgelist(filename, create_using=nx.DiGraph)
        # Output whether it has cycles
        print(f"Graph {filename} has cycles: {has_cycles(G)}")
