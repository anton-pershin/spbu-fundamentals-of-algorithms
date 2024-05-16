import networkx as nx
from src.plotting import plot_graph

TEST_GRAPH_FILES = [
    "practicum_2/homework/basic/graph_1_wo_cycles.edgelist",
    "practicum_2/homework/basic/graph_2_wo_cycles.edgelist",
    "practicum_2/homework/basic/graph_3_wo_cycles.edgelist",
]

def has_cycles(g: nx.Graph):
    return len(nx.cycle_basis(g)) > 0

if __name__ == "__main__":
    for filename in TEST_GRAPH_FILES:
        # Load the graph
        G = nx.read_edgelist(filename, create_using=nx.Graph)
        # Output whether it has cycles
        print(f"Graph {filename} has cycles: {has_cycles(G)}")
        plot_graph (G)