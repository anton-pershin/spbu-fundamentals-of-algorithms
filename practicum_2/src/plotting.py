from typing import Union, Any

import matplotlib.pyplot as plt
import networkx as nx


def plot_graph(G: Union[nx.Graph, nx.DiGraph] = None) -> None:
    fig, ax = plt.subplots(figsize=(10, 5))
    pos = nx.spring_layout(G)

    options = dict(
        font_size=10,
        node_size=250,
        node_color="white",
        edgecolors="black",
    )
    
    nx.draw_networkx(G, pos, ax=ax, **options)
    if nx.is_weighted(G):
        labels = {e: G.edges[e]["weight"] for e in G.edges}
        nx.draw_networkx_edge_labels(G, pos, ax=ax, edge_labels=labels)
    plt.show()
