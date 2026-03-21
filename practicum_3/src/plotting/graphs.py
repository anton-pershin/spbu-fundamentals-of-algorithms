from typing import Any

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import plotly.graph_objects as go
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout


def plot_graph(
    G, 
    node_weights=None,
    figsize=(6, 5),
    name=None,
    highlighted_edges: list[tuple[Any, Any]] = None
):
    fig, ax = plt.subplots(1, 1, figsize=figsize)
    edge_color_list = ["black"] * len(G.edges)
    if highlighted_edges:
        for i, edge in enumerate(G.edges()):
            if edge in highlighted_edges or (edge[1], edge[0]) in highlighted_edges:
                edge_color_list[i] = "red"

    options = dict(
        ax=ax,
        font_size=12,
        node_size=500,
        edgecolors="black",
        edge_color=edge_color_list,
    )
    
    if node_weights is not None:
        # Normalize weights to [0; 1] for colormap
        weights = np.array([node_weights.get(node, 0) for node in G.nodes()])
        norm = plt.Normalize(vmin=weights.min(), vmax=weights.max())
        cmap = plt.cm.viridis
        minval = 0.2
        maxval = 1.0
        n = 100
        truncated_cmap = colors.LinearSegmentedColormap.from_list(
            "trunc({n},{a:.2f},{b:.2f})".format(n=cmap.name, a=minval, b=maxval),
            cmap(np.linspace(minval, maxval, n))
        )
        options["node_color"] = [truncated_cmap(norm(w)) for w in weights]
    else:
        options["node_color"] = "white"
    
    
    pos = nx.spring_layout(G)
    nx.draw_networkx(G, pos, **options)
    if nx.is_weighted(G):
        labels = {e: G.edges[e]["weight"] for e in G.edges}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        
    if node_weights is not None:
        sm = plt.cm.ScalarMappable(cmap=truncated_cmap, norm=norm)
        sm.set_array([])
        plt.colorbar(sm)

    if name is not None:
        ax.set_title(name)

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


def plot_network_via_plotly(G, pos, name):
    """
    Borrowed from https://plotly.com/python/network-graphs/
    """
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color="#888"),
        hoverinfo="none",
        mode="lines")

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode="markers",
        hoverinfo="text",
        marker=dict(
            showscale=True,
            colorscale="YlGnBu",
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title=dict(
                  text="Degree",
                  side="right"
                ),
                xanchor="left",
            ),
            line_width=2
        )
    )

    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append(f"Degree: {len(adjacencies[1])}")

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text

    fig = go.Figure(data=[edge_trace, node_trace],
                 layout=go.Layout(
                    title=dict(
                        font=dict(
                            size=16
                        )
                    ),
                    showlegend=False,
                    hovermode="closest",
                    margin=dict(b=20,l=5,r=5,t=40),
                    annotations=[ dict(
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002 ) ],
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                 )
    )
    fig.write_html(f"{name}.html")

