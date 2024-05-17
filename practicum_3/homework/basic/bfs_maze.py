import networkx as nx
import numpy as np
from typing import Any


class Maze:
    def __init__(self, list_view: list[list[str]]) -> None:
        self.list_view = list_view
        self.start_j = None
        self.end_coords = None
        self.graph = None
        for j, sym in enumerate(self.list_view[0]):
            if sym == "O":
                self.start_j = j
        for j, sym in enumerate(self.list_view[-1]):
            if sym == "X":
                self.end_coords = f"{len(list_view) - 1},{j}"

    @classmethod
    def from_file(cls, filename):
        list_view = []
        with open(filename, "r") as f:
            for l in f.readlines():
                list_view.append(list(l.strip()))
        obj = cls(list_view)
        return obj

    @staticmethod
    def dijkstra_sp(G: nx.Graph, source_node) -> dict[Any, list[Any]]:
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

    def parse_graph(self) -> None:
        graph = nx.Graph()
        for i in range(len(self.list_view)):
            for j in range(len(self.list_view[0])):
                if self.list_view[i][j] != "#":
                    graph.add_node(f"{i},{j}")
                    try:
                        if self.list_view[i+1][j] != "#":
                            graph.add_edge(f"{i},{j}", f"{i+1},{j}", weight=1)
                        if self.list_view[i][j+1] != "#":
                            graph.add_edge(f"{i},{j}", f"{i},{j+1}", weight=1)
                    except:
                        pass
        self.graph = graph

    @staticmethod
    def sp_to_LRUD(path: list[str]) -> list[str]:
        LRUD_path = []
        for i in range(len(path) - 1):
            l_s, r_s = map(int, path[i].split(","))
            l_f, r_f = map(int, path[i+1].split(","))
            vertical = l_s - l_f
            horizontal = r_s - r_f
            LRUD_path.append(Maze.shift_coordinate(horizontal, vertical))
        return LRUD_path

    @classmethod
    def shift_coordinate(cls, i, j) -> str:
        if j == -1:
            return "D"
        elif j == 1:
            return "U"
        elif i == -1:
            return "R"
        else:
            return "L"


def solve(maze: Maze) -> None:
    maze.parse_graph()
    path = Maze.dijkstra_sp(maze.graph, source_node=f"0,{maze.start_j}")
    path = Maze.sp_to_LRUD(path[maze.end_coords])

    print(f"Founded path: {"".join(path)}")


if __name__ == "__main__":
    maze = Maze.from_file("C://Users//User//Desktop//qq//spbu-fundamentals-of-algorithms//practicum_3//homework//basic//maze_2.txt")
    maze.parse_graph()
    solve(maze)
