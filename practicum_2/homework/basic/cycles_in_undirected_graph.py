import networkx as nx


def has_cycles(G: nx.Graph, v: str, prev_v: str, visited: list[bool]) -> None:
    global flag

    if not visited[int(v)]:
        visited[int(v)] = True
    else:
        flag = True
        return

    for neighbor in G[v]:
        if neighbor != prev_v:
            has_cycles(G, neighbor, v, visited)


TEST_GRAPH_FILES = [
    "graph_1_wo_cycles.edgelist.txt",
    "graph_2_w_cycles.edgelist.txt",
]

if __name__ == "__main__":
    for filename in TEST_GRAPH_FILES:
        # Load the graph
        G = nx.read_edgelist(f"C://Users//User//Алгоритмы//{filename}", create_using=nx.Graph)

        # Output whether it has cycles
        flag = False
        visited = [False] * len(G)
        has_cycles(G, "0", "0", visited)
        
        if flag:
            print(f"Graph {filename} has cycles")
        else:
            print(f"Graph {filename} has no cycles") 
