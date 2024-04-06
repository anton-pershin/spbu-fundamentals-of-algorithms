import networkx as nx
from src.plotting import plot_graph

TEST_GRAPH_FILES = [
    "practicum_2/homework/advanced/graph_1_wo_cycles.edgelist",
    "practicum_2/homework/advanced/graph_2_wo_cycles.edgelist",
    "practicum_2/homework/advanced/graph_3_wo_cycles_edgelist",
]

def has_cycles(g: nx.DiGraph):
    try:
        cycle = nx.find_cycle(g)
        return True
    except nx.NetworkXNoCycle:
        return False

if __name__ == "__main__":
    for filename in TEST_GRAPH_FILES:
        # Load the graph
        G = nx.read_edgelist(filename, create_using=nx.DiGraph)
        # Output whether it has cycles
        print(f"Graph {filename} has cycles: {has_cycles(G)}")