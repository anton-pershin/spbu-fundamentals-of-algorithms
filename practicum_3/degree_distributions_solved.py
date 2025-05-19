from pathlib import Path
file_path = "USairport500.txt"

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

from src.plotting.graphs import plot_graph, plot_network_via_plotly
from src.common import NDArrayFloat


def build_degree_histogram(G) -> tuple[NDArrayFloat, NDArrayFloat]:
    degrees = [node_degree for _, node_degree in G.degree()]
    hist, bin_edges = np.histogram(degrees, bins=20)
    mids = 0.5*(bin_edges[:-1] + bin_edges[1:])
    return hist, mids


if __name__ == "__main__":
    # USairport500.txt stores a network of the most active US airports.
    # This is a typical example of a scale-free network as some airports
    # are known to be hubs
    G_airports = nx.read_edgelist(file_path, nodetype=int, data=(("weight", float),))
    pos = nx.spring_layout(G_airports)
    plot_network_via_plotly(G=G_airports, pos=pos, name="airports")

    # Erdos-Renyi graphs are in turn have no hubs
    G_er = nx.erdos_renyi_graph(n=1000, p=0.02, directed=False)
    pos = nx.spring_layout(G_er)
    plot_network_via_plotly(G=G_er, pos=pos, name="er")

    # Let's look at the degree distributions for each graphs
    # to confirm our claims
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    for G, label in zip((G_airports, G_er), ("US airports", "Erdos-Renyi graph")):
        hist, mids = build_degree_histogram(G)
        ax.loglog(mids, hist, "o--", label=label)
    ax.set_xlabel(r"$k$", fontsize=12)
    ax.set_ylabel(r"$f(k)$", fontsize=12)
    ax.grid()
    ax.legend(fontsize=12)
    fig.tight_layout()
    plt.show()

