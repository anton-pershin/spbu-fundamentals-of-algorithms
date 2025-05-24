from typing import Any, Protocol
from itertools import combinations

import numpy as np
import networkx as nx

import matplotlib.pyplot as plt


class CentralityMeasure(Protocol):
    def __call__(self, G: nx.Graph) -> dict[Any, float]:
        ...

def plot_graph(G: nx.Graph, node_weights: dict[Any, float], figsize=(14, 8), name: str = ""):
    plt.figure(figsize=figsize)
    pos = nx.spring_layout(G, seed=42)  
    nx.draw_networkx_nodes(
        G, pos, 
        node_color=list(node_weights.values()), 
        cmap=plt.cm.viridis, 
        node_size=500,
        alpha=0.8
    )
    nx.draw_networkx_edges(G, pos, alpha=0.3)
    nx.draw_networkx_labels(G, pos)
    

    
    plt.title(f"{name} Centrality")
    plt.axis("off")
    plt.show()

def closeness_centrality(G: nx.Graph) -> dict[Any, float]:
    centrality = {}
    nodes = G.nodes()
    for node in nodes:
        sum_sp = 0
        for other_node in nodes:
            if node != other_node:
                sum_sp += nx.shortest_path_length(G, source=node, target=other_node)
    
        if sum_sp > 0:
            centrality[node] = (len(nodes) - 1) / sum_sp
        else:
            centrality[node] = 0.0
    return centrality



def betweenness_centrality(G: nx.Graph) -> dict[Any, float]:
    centrality = {node: 0.0 for node in G.nodes()}
    nodes = list(G.nodes())
    
    for s, t in combinations(nodes, 2):
            
            all_paths = list(nx.all_shortest_paths(G, source=s, target=t))

            for path in all_paths:
                for node in path[1:-1]:
                    centrality[node] += 1.0

    return centrality


def eigenvector_centrality(G: nx.Graph) -> dict[Any, float]:
    adjacency_matrix = nx.to_numpy_array(G)
    eigenvalues, eigenvectors = np.linalg.eig(adjacency_matrix)
    
    max_ind = np.argmax(eigenvalues)
    principal_eigenvector = eigenvectors[:, max_ind]
    
    centrality = {}
    nodes = list(G.nodes())
    for i, node in enumerate(nodes):
        centrality[node] = float(principal_eigenvector[i])

    max_val = max(centrality.values())
    if max_val > 0:
        for node in centrality:
            centrality[node] /= max_val
    return centrality

def plot_centrality_measure(G: nx.Graph, measure: CentralityMeasure) -> None:
    values = measure(G)
    if values is not None:
        plot_graph(G, node_weights=values, figsize=(14, 8), name=measure.__name__)
    else:
        print(f"Implement {measure.__name__}")


if __name__ == "__main__":
    G = nx.karate_club_graph()
    plot_centrality_measure(G, closeness_centrality)
    plot_centrality_measure(G, betweenness_centrality)
    plot_centrality_measure(G, eigenvector_centrality)



