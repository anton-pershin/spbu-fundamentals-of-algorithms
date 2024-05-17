import networkx as nx

TEST_GRAPH_FILES = [
    "graph_1_wo_cycles.edgelist",
    "graph_2_w_cycles.edgelist",
]


def has_cycles(g: nx.Graph):
    def dfs(v, parent):
        visited.add(v)
        for neighbor in g.neighbors(v):
            if neighbor not in visited:
                if dfs(neighbor, v):
                    return True
            elif parent != neighbor:
                return True
        return False

    visited = set()
    for node in g.nodes:
        if node not in visited:
            if dfs(node, None):
                return True
    return False


if __name__ == "__main__":
    for filename in TEST_GRAPH_FILES:
        G = nx.read_edgelist("C:/IT/algorithms/spbu-fundamentals-of-algorithms/practicum_2/homework/basic/" + filename,
                             create_using=nx.Graph)
        if has_cycles(G):
            print(f"Graph {filename} has cycles: YES")
        else:
            print(f"Graph {filename} has cycles: NO")