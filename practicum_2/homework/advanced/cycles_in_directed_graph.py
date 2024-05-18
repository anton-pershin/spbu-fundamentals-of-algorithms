import os

import networkx as nx

TEST_GRAPH_FILES = [
    "graph_1_wo_cycles.edgelist",
    "graph_2_wo_cycles.edgelist",
    "graph_3_w_cycles_edgelist"
]


def cycle_check(g, node, visited, stack):
    visited[node] = True  # отмечаем вершину как посещённую
    stack[node] = True  # и кладём её в стек

    for neighbor in g.neighbors(str(node)):  # проходимся по всем соседям вершины
        if not visited[int(neighbor)]:  # если мы её ещё не посещали, то...
            if cycle_check(g, int(neighbor), visited, stack):  # заходим в неё
                return True
        elif stack[int(neighbor)]:  # чтобы граф был зацикленным, нам необходимо, чтобы вершина имела своего
            # "предка" в качестве соседа
            return True
    stack[node] = False  # возвращаемся обратно из этой вершины, подчищая стек
    return False


def has_cycles(g: nx.DiGraph):
    length = g.number_of_nodes()  # инициализация...
    visited = [False] * length
    stack = [False] * length
    for node in range(length):  # проходимся по всем нодам
        if cycle_check(g, node, visited, stack):  # воспользуемся вспомогательной функцией
            return True
    return False


if __name__ == "__main__":
    for filename in TEST_GRAPH_FILES:
        # Load the graph

        G = nx.read_edgelist(filename, create_using=nx.DiGraph)

        G = nx.read_edgelist(
            os.path.join("practicum_2", "homework", filename), create_using=nx.DiGraph
        )

        # Output whether it has cycles
        print(f"Graph {filename} has cycles: {has_cycles(G)}")
