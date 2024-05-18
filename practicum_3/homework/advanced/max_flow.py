from typing import Any
from typing import Union
from collections import deque
import time
from queue import PriorityQueue
import numpy as np

import matplotlib.pyplot as plt

import networkx as nx

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


def max_flow(G: nx.Graph, s: Any, t: Any) -> int:
    value: int = 0
    
    min_flow: int = 0
    queue = deque([[str(s)]])
    flows = deque([[np.inf]])

    while queue:
        current_flows = flows.popleft()
        current_path = queue.popleft()
        current_node = current_path[-1]
        if current_node == str(t):
            min_flow = min(current_flows)
            flag = True
            G1 = G.copy()
            for n in range(0, len(current_path) - 1):
                G[current_path[n]][current_path[n+1]]['weight'] -= min_flow
                if G[current_path[n]][current_path[n+1]]['weight'] < 0:
                    flag = False
                    break
            if flag:
                value += min_flow
            else:
                G = G1
            
        else:
            for neighbor in G.neighbors(current_node):
                if neighbor not in current_path:
                    flows.append(current_flows + [G[current_node][neighbor]['weight']])
                    queue.append(current_path + [neighbor])

                    
                    

    return value


if __name__ == "__main__":
    # Load the graph
    G = nx.read_edgelist("practicum_3/homework/advanced/graph_1.edgelist", create_using=nx.DiGraph)
    #plot_graph(G)
    val = max_flow(G, s=0, t=5)
    print(f"Maximum flow is {val}. Should be 23") 