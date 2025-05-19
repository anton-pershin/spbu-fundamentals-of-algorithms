import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

from src.plotting.graphs import plot_graph, plot_network_via_plotly
from src.common import NDArrayFloat


def build_degree_histogram(G) -> tuple[NDArrayFloat, NDArrayFloat]:
    degrees = [G.degree(node) for node in G.nodes()]
    hist, bins = np.histogram(degrees, bins=range(max(degrees) + 2))
    mids = (bins[:-1] + bins[1:]) / 2
    return hist, mids


if __name__ == "__main__":
    # USairport500.txt stores a network of the most active US airports.
    # This is a typical example of a scale-free network as some airports
    # are known to be hubs
    G_airports = nx.read_edgelist(Path("practicum_3") / "USairport500.txt", nodetype=int, data=(("weight", float),))
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
        res = build_degree_histogram(G)
        if res is not None:
            hist, mids = res
        else:
            print("Implement build_degree_histogram")
            sys.exit()
        ax.loglog(mids, hist, "o--", label=label)
    ax.set_xlabel(r"$k$", fontsize=12)
    ax.set_ylabel(r"$f(k)$", fontsize=12)
    ax.grid()
    ax.legend(fontsize=12)
    fig.tight_layout()
    plt.show()

