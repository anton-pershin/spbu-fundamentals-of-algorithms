import matplotlib.pyplot as plt
import networkx as nx

TEST_GRAPH_FILES = [
    "graph_1_wo_cycles.edgelist",
    "graph_2_w_cycles.edgelist",
]


def plot_graph(G):
    options = dict(
        font_size=12,
        node_size=500,
        node_color="white",
        edgecolors="black",
    )
    pos = nx.spring_layout(G)
    nx.draw_networkx(G, pos, **options)
    if nx.is_weighted(G):
        labels = {e: G.edges[e]['weight'] for e in G.edges}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.show()

def has_cycles_dfs_algorithm(G: nx.Graph):
    global flag
    # состояния node: 0 ("Белая точка") - ещё не посетили точку, 1 ("Серая точка") - точка открыта (посетили точку), 
    # 2 ("Чёрная точка") - точка закрыта (посетили всё поддерево, узлом которого является эта node)
    colour = [0] * len(G)
    # parent - узел, из которого мы пришли в эту node
    parent = [None] * len(G)
    
    def dfs_visit(node):
        global flag
        colour[int(node)] = 1
        for i in G.neighbors(node):
            if colour[int(i)] == 0:
                parent[int(i)] = node
                for j in G.neighbors(i):
                    if (colour[int(j)] == 1 or colour[int(j)] == 2) and (j != parent[int(i)]): #Если сосед (серый или чёрный) и он не родитель - есть цикл
                        flag = False
                dfs_visit(i)
        colour[int(node)] = 2
    
    flag = True
    for node in G:
        if colour[int(node)] == 0:
            dfs_visit(node)
    
    return flag

if __name__ == "__main__":
    for filename in TEST_GRAPH_FILES:
        G = nx.read_edgelist("D:/spbu-fundamentals-of-algorithms/practicum_2/homework/basic/" + filename, create_using=nx.Graph)
        plot_graph(G)
        if has_cycles_dfs_algorithm(G):
            print(f"Graph {filename} has cycles: NO")
        else:
            print(f"Graph {filename} has cycles: YES")
