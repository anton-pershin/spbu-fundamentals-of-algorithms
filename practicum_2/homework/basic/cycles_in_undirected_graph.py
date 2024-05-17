import os
import networkx as nx
from typing import Union, Any
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout
import numpy as np
from numpy.typing import NDArray
NDArrayInt = NDArray[np.int_]
def plot_graph(
    G: Union[nx.Graph, nx.DiGraph], highlighted_edges: list[tuple[Any, Any]] = None
) -> None:
    fig, ax = plt.subplots(figsize=(12, 6))
    pos = nx.spring_layout(G)
    edge_color_list = ["black"] * len(G.edges)
    if highlighted_edges:
        for i, edge in enumerate(G.edges()):
            if edge in highlighted_edges or (edge[1], edge[0]) in highlighted_edges:
                edge_color_list[i] = "red"
    options = dict(
        font_size=12,
        node_size=500,
        node_color="white",
        edgecolors="black",
        edge_color=edge_color_list,
    )
    nx.draw_networkx(G, pos, ax=ax, **options)
    if nx.is_weighted(G):
        labels = {e: G.edges[e]["weight"] for e in G.edges}
        nx.draw_networkx_edge_labels(G, pos, ax=ax, edge_labels=labels)
    plt.show()


def plot_tree(G: nx.DiGraph) -> None:
    fig, ax = plt.subplots(figsize=(12, 6))
    pos = graphviz_layout(G, prog="dot")
    options = dict(
        font_size=12,
        node_size=500,
        node_color="white",
        edgecolors="black",
    )
    nx.draw_networkx(G, pos, ax=ax, **options)
    plt.show()


TEST_GRAPH_FILES = [
    "graph_1_wo_cycles.edgelist",
    "graph_2_w_cycles.edgelist",
]


def has_cycles(g: nx.Graph):
    visited = set()
    cycle = False

    def dfs(node, parent):
        nonlocal cycle
        visited.add(node)

        for neighbor in g.neighbors(node):
            if neighbor not in visited:
                dfs(neighbor, node)
            elif neighbor != parent:  # Найден цикл
                cycle = True

    for node in g.nodes():
        if node not in visited:
            dfs(node, None)

    return cycle


    


if __name__ == "__main__":
    for filename in TEST_GRAPH_FILES:
        # Load the graph
        G = nx.read_edgelist("practicum_2/homework/basic/" + filename)
        plot_graph(G)
        # Output whether it has cycles
        print(f"Graph {filename} has cycles: {has_cycles(G)}")
