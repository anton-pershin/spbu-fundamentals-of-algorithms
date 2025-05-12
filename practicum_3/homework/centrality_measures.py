from typing import Any, Protocol
from itertools import combinations

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from src.plotting.graphs import plot_graph, plot_network_via_plotly
from src.common import AnyNxGraph 


class CentralityMeasure(Protocol):
    def __call__(self, G: AnyNxGraph) -> dict[Any, float]:
        ...


def closeness_centrality(G: AnyNxGraph) -> dict[Any, float]:
    centrality = {}
    n = len(G.nodes())
    
    for node in G.nodes():
        total_dist = 0
        for other_node in G.nodes():
            if node != other_node:
                try:
                    total_dist += nx.shortest_path_length(G, source=node, target=other_node)
                except nx.NetworkXNoPath:
                    pass
        if total_dist > 0:
            centrality[node] = (n - 1) / total_dist  
        else:
            centrality[node] = 0
            
    return centrality




def betweenness_centrality(G: AnyNxGraph) -> dict[Any, float]: 

    centrality = {node: 0.0 for node in G.nodes()}
    nodes = list(G.nodes())
    
    for s, t in combinations(nodes, 2):
        try:
            all_paths = list(nx.all_shortest_paths(G, source=s, target=t))
        except nx.NetworkXNoPath:
            continue
            
        if not all_paths:
            continue
            
        s = len(all_paths) 
        for path in all_paths:
            for v in path[1:-1]:  
                centrality[v] += 1.0 / s
    if not nx.is_directed(G):
        n = len(nodes)
        sc = 2.0 / ((n - 1) * (n - 2)) if n > 2 else 1.0
    else:
        n = len(nodes)
        sc = 1.0 / ((n - 1) * (n - 2)) if n > 2 else 1.0
        
    for node in centrality:
        centrality[node] *= sc
        
    return centrality


def eigenvector_centrality(G: AnyNxGraph) -> dict[Any, float]: 

    nodes = list(G.nodes())
    
    A = nx.to_numpy_array(G, nodelist=nodes)

    eigenvalues, eigenvectors = np.linalg.eig(A)

    max_idx = np.argmax(np.abs(eigenvalues))
    principal_eigenvector = eigenvectors[:, max_idx].real

    norm = np.linalg.norm(principal_eigenvector)
    if norm > 0:
        principal_eigenvector = principal_eigenvector / norm
    centrality = {node: principal_eigenvector[i] for i, node in enumerate(nodes)}
    
    return centrality


def plot_centrality_measure(G: AnyNxGraph, measure: CentralityMeasure) -> None:
    values = measure(G)
    if not values:
        print(f"Implement {measure.__name__}")
        return

    fig, ax = plt.subplots(figsize=(14, 8))

    min_val = min(values.values())
    max_val = max(values.values())
    normalized_values = {k: (v - min_val)/(max_val - min_val) if max_val != min_val else 0.5 
                        for k, v in values.items()}

    pos = nx.spring_layout(G)
    nodes = nx.draw_networkx_nodes(
        G, pos, 
        node_color=list(normalized_values.values()),
        cmap=plt.cm.viridis,
        node_size=500,
        ax=ax
    )
    nx.draw_networkx_edges(G, pos, ax=ax)
    nx.draw_networkx_labels(G, pos, ax=ax)

    sm = plt.cm.ScalarMappable(
        cmap=plt.cm.viridis,
        norm=plt.Normalize(vmin=min_val, vmax=max_val)
    )
    sm._A = [] 
    plt.colorbar(sm, ax=ax)
    
    ax.set_title(measure.__name__)
    plt.tight_layout()
    plt.show()



if __name__ == "__main__":
    G = nx.karate_club_graph()
    
    plot_centrality_measure(G, closeness_centrality)
    plot_centrality_measure(G, betweenness_centrality)
    plot_centrality_measure(G, eigenvector_centrality)
