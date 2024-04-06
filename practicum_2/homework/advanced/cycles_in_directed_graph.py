import networkx as nx
from typing import Any
from src.plotting import plot_graph

TEST_GRAPH_FILES = [
    "graph_1_wo_cycles.edgelist",
    "graph_2_wo_cycles.edgelist",
    "graph_3_wo_cycles.edgelist",
]

#Frozenset (замороженное множество) – это класс с характеристиками множества,
#но элементы нельзя менять после объявления.

#Зачем выходить из рекурсии, если можно найти все циклы сразу:
def has_cycles(G: nx.DiGraph, node: Any, visited: set, covered_nodes: set, cycles: set):

    visited.add(node)
    covered_nodes.add(node)

    for neighbor in G.neighbors(node):
        if neighbor in covered_nodes:
            cycles.add(frozenset(covered_nodes)) #хз почему обычный set не подходит
        if neighbor not in visited:
            has_cycles(G, neighbor, visited, covered_nodes, cycles)

    covered_nodes.remove(node)

    return len(cycles)

if __name__ == "__main__":
    for filename in TEST_GRAPH_FILES:
        # Load the graph
        G = nx.read_edgelist(filename, create_using=nx.DiGraph)


        visited = set()
        covered_nodes = set()
        cycles = set()

        answer = has_cycles(G, "0", visited, covered_nodes, cycles)
        if (answer != 0):
            print(f"Graph {filename} has cycles: {answer}: {cycles} 😇")
            plot_graph(G)
        else:
            print(f"Graph {filename} hasn't got cycles 😔")