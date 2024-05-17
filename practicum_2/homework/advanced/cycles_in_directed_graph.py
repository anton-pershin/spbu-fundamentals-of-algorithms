import networkx as nx

TEST_GRAPH_FILES = [
    "graph_1_wo_cycles.edgelist",
    "graph_2_wo_cycles.edgelist",
    "graph_3_w_cycles_edgelist"
]


def dfs(g: nx.DiGraph, node, finish, count):
    for neighbor in g.neighbors(node):
        if neighbor == finish:
            return 1
        count += dfs(g, neighbor, finish, 0)
    return count

def has_cycles(g: nx.DiGraph):
    result = 0
    for node in g:
        for neighbor in g.neighbors(node):
            result += dfs(g, neighbor, node, 0)
    return bool(result)


if __name__ == "__main__":
    for filename in TEST_GRAPH_FILES:
        # Load the graph
        G = nx.read_edgelist(filename, create_using=nx.DiGraph)
        # Output whether it has cycles
        print(f"Graph {filename} has cycles: {has_cycles(G)}")
