import networkx as nx

TEST_GRAPH_FILES = [
    "graph_1_wo_cycles.edgelist",
    "graph_2_w_cycles.edgelist",
]

def has_cycles(g: nx.DiGraph):
    cycles = list(nx.simple_cycles(g)) # nx.simple_cycles() ищет все простые циклы
    return len(cycles) > 0

if __name__ == "__main__":
    for filename in TEST_GRAPH_FILES:
        # Load the graph
        G = nx.read_edgelist("practicum_2/graph_2.edgelist", create_using=nx.DiGraph)
        # Output whether it has cycles
        print(f"Graph {filename} has cycles: {has_cycles(G)}")
