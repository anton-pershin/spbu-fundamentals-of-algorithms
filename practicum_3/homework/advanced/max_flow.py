from typing import Any
from collections import deque
from src.plotting import plot_graph

import networkx as nx

TEST_GRAPH_FILES = [
    "graph_1.edgelist",
    "graph_2.edgelist",
]
def legitcheck(W: nx.DiGraph, s: Any, t: Any) -> Any: # Функция проверки правильности работы алгоритма для любого графа

    flow_value, flow_dict = nx.maximum_flow(W, s, t, capacity='weight')
    return flow_value


def bfs(G: nx.DiGraph, s: Any, t: Any, parent: dict[Any]) -> Any:

    if s not in G.nodes:
        raise ValueError(f"The NODE {s} is not in the graph.")

    visited = {n: False for n in G}
    visited[s] = True
    queue = deque([s])

    while queue:
        node = queue.popleft()
        for neighbour in G.neighbors(node):
            if not visited[neighbour] and G[node][neighbour]['weight'] > 0:
                visited[neighbour] = True
                parent[neighbour] = node
                if neighbour == t:
                        return True
                queue.append(neighbour)

    return False


def max_flow(G: nx.DiGraph, s: Any, t: Any) -> Any:
    answer = 0
    parent = {n: None for n in G}
    G_reverse = G.reverse() # Reverse the graph

    for a, b, data in G_reverse.edges(data=True):
        G_reverse[a][b]['weight'] = 0


    while bfs(G, s, t, parent):
        path_flow = float('inf')

        node = t
        while node != s:
            parent_node = parent[node]
            path_flow = min(G[parent_node][node]['weight'], path_flow)
            node = parent_node

        answer += path_flow

        node = t
        while node != s:
            parent_node = parent[node]
            G_reverse[node][parent_node]['weight'] += path_flow
            G[parent_node][node]['weight'] -= path_flow
            node = parent_node

    return answer#, G, G_reverse


if __name__ == "__main__":

    for filename in TEST_GRAPH_FILES:
        G = nx.read_edgelist(filename, create_using=nx.DiGraph)
        W = nx.read_edgelist(filename, create_using=nx.DiGraph)

        val= max_flow(G, s='0', t='5')
        legit = legitcheck(W, s='0', t='5')

        print(f"Maximum flow is {val}. Should be 23") #{legit}")
        print("-"*50)

        # print("Визуализация максимального потока:")
        # plot_graph(Q) # Визуализация максимального потока
        #
        # print("-"*50)
        #
        # print("Визуализация остаточного графа:")
        # plot_graph(Q_reverse) # Визуализация остаточного графа
        #
        # print("-"*50)


    # Время работы алгоритма Эдмондса-Карпа - O(V(E^2))


#%%
