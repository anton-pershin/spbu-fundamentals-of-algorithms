import networkx as nx
from typing import Any

TEST_GRAPH_FILES = [
    "practicum_2\homework\\advanced\graph_1_wo_cycles.edgelist",
    "practicum_2\homework\\advanced\graph_2_wo_cycles.edgelist",
    "practicum_2\homework\\advanced\graph_3_w_cycles_edgelist",
]

def has_cycles(g: nx.DiGraph):
    if (sorted(nx.simple_cycles(G)) != []):
        return True
    return False


if __name__ == "__main__":
    for filename in TEST_GRAPH_FILES:
        # Load the graph
        G = nx.read_edgelist(filename, create_using=nx.DiGraph)
        # Output whether it has cycles
        print(f"Graph {filename} has cycles: {has_cycles(G)}")
