from operator import itemgetter, ne
from queue import PriorityQueue
from typing import Any

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

from src.plotting import plot_graph


def dijkstra_sp_with_priority_queue(
    G: nx.Graph, source_node="0"
) -> dict[Any, list[Any]]:
    # unvisited_set = set()
    visited_set = set()
    shortest_paths = {}  # key = destination node, value = list of intermediate nodes
    dist = {n: np.inf for n in G}
    dist[source_node] = 0
    shortest_paths[source_node] = [source_node]

    pq = PriorityQueue()
    pq.put((dist[source_node], source_node))
    while not pq.empty():
        min_dist, node = pq.get()
        visited_set.add(node)
        for neigh_node in G.neighbors(node):
            if neigh_node in visited_set:
                continue
            new_dist = min_dist + G.edges[node, neigh_node]["weight"]
            if new_dist < dist[neigh_node]:
                dist[neigh_node] = new_dist
                shortest_paths[neigh_node] = shortest_paths[node] + [neigh_node]
                pq.put((new_dist, neigh_node))
    return shortest_paths


def dijkstra_sp(G: nx.Graph, source_node="0") -> dict[Any, list[Any]]:
    unvisited_set = set(G.nodes())
    visited_set = set()
    shortest_paths = {}  # key = destination node, value = list of intermediate nodes
    dist = {n: np.inf for n in G}
    dist[source_node] = 0
    shortest_paths[source_node] = [source_node]

    while unvisited_set:
        node = None
        min_dist = np.inf
        for n, d in dist.items():
            if (n in unvisited_set) and (d < min_dist):
                min_dist = d
                node = n
        unvisited_set.remove(node)
        visited_set.add(node)
        for neigh_node in G.neighbors(node):
            if neigh_node in visited_set:
                continue
            new_dist = min_dist + G.edges[node, neigh_node]["weight"]
            if new_dist < dist[neigh_node]:
                dist[neigh_node] = new_dist
                shortest_paths[neigh_node] = shortest_paths[node] + [neigh_node]
    return shortest_paths


if __name__ == "__main__":
    G = nx.read_edgelist("practicum_3/graph_1.edgelist", create_using=nx.Graph)
    plot_graph(G)
    shortest_paths = dijkstra_sp_with_priority_queue(G, source_node="0")
    # shortest_paths = dijkstra_sp(G, source_node="0")
    test_node = "5"
    shortest_path_edges = [
        (shortest_paths[test_node][i], shortest_paths[test_node][i + 1])
        for i in range(len(shortest_paths[test_node]) - 1)
    ]
    plot_graph(G, highlighted_edges=shortest_path_edges)
    print()
