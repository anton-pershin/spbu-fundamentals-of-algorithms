import networkx as nx



TEST_GRAPH_FILES = [
    "graph_1_wo_cycles.edgelist",
    "graph_2_w_cycles.edgelist",
]


def has_cycles(g: nx.Graph, root, parents:list[int], status:list[int]):
    not_visited = 0; visited = 1; double_visited = -1;
    status[int(root)] = visited
    answer = True
    while answer == True:
        for i in g.neighbors(root):
            if status[int(i)] == not_visited :
                 parents[int(i)] = root #чтобы не попасть туда же
                 for j in g.neighbors(i):
                    if ( j != root[int(i) & status[int(j)] == visited]):
                        answer = False
    return answer


if __name__ == "__main__":
    for filename in TEST_GRAPH_FILES:
        #G = nx.read_edgelist(f"D://algorithm//spbu-fundamentals-of-algorithms//practicum_2//homework//basic//{filename}", create_using=nx.Graph)
        # Output whether it has cycles
        G = nx.read_edgelist(f"C://Users/Alexandra//Documents//Универ//Algos//fundamentals-of-algorithms//practicum_2//homework//basic//{filename}", create_using=nx.Graph)
        answer = True
        for i in G:
            status = [0] * len(G)
            parents = [0] * len(G)
            while answer != False:
                if has_cycles(G, i, status, parents) == False:
                    answer = False
    if answer == False:
            print(f"Graph {filename} is cycled")
    else:
            print(f"Graph {filename} is acycled")
