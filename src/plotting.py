from typing import Union, Any

import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout
import numpy as np
from numpy.typing import NDArray

from src.common import NDArrayInt


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


def plot_points(points: NDArray, convex_hull: NDArray = None, **kwargs) -> None:
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(points[:, 0], points[:, 1], "o", **kwargs)
    if convex_hull is not None:
        convex_hull = np.concatenate(
            (convex_hull, convex_hull[0, :].reshape(1, -1)), axis=0
        )
        ax.plot(convex_hull[:, 0], convex_hull[:, 1], "-", linewidth=4, zorder=-10)
    ax.grid()
    fig.tight_layout()
    plt.show()


def plot_loss_history(
    loss_history: NDArrayInt, xlabel="# iterations", ylabel="# conflicts"
) -> None:
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    if loss_history.ndim == 1:
        loss_history = loss_history.reshape(1, -1)
    n_restarts, n_iters = loss_history.shape
    for i in range(n_restarts):
        ax.plot(range(n_iters), loss_history[i, :])
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid()
    fig.tight_layout()
    plt.show()
