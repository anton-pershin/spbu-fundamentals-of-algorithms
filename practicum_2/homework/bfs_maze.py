from time import perf_counter
import networkx as nx
from queue import Queue

class Maze:
    def __init__(self, list_view: list[list[str]]) -> None:
        self.list_view = list_view
        self.start_j = None
        for j, sym in enumerate(self.list_view[0]):
            if sym == "O":
                self.start_j = j

    @classmethod
    def from_file(cls, filename):
        list_view = []
        with open(filename, "r") as f:
            for l in f.readlines():
                list_view.append(list(l.strip()))
        obj = cls(list_view)
        return obj

    def print(self, path="") -> None:
        # Find the path coordinates
        i = 0  # in the (i, j) pair, i is usually reserved for rows and j is reserved for columns
        j = self.start_j
        path_coords = set()
        for move in path:
            i, j = _shift_coordinate(i, j, move)
            path_coords.add((i, j))
        # Print maze + path
        for i, row in enumerate(self.list_view):
            for j, sym in enumerate(row):
                if (i, j) in path_coords:
                    print("+ ", end="")  # NOTE: end is used to avoid linebreaking
                else:
                    print(f"{sym} ", end="")
            print()  # linebreak


def solve(maze: Maze) -> None:
    path = ""  # solution as a string made of "L", "R", "U", "D"

    # creating graph
    G = nx.Graph()
    edges = []
    X = None

    # adding edges in graph, given that the number of each cell is its serial number from 0 to n*m - 1
    for i in range(len(maze.list_view)):
        for j in range(len(maze.list_view[i])):
            if maze.list_view[i][j] in " X":
                if i > 0 and maze.list_view[i - 1][j] in " O":
                    edges.append(((i - 1) * len(maze.list_view) + j, i * len(maze.list_view) + j))
                if j > 0 and maze.list_view[i][j - 1] == " ":
                    edges.append((i * len(maze.list_view) + j - 1, i * len(maze.list_view) + j))
                if maze.list_view[i][j] == "X":
                    X = i * len(maze.list_view) + j

    # writing auxiliary data structures for bfs
    G.add_edges_from(edges)
    visited = {}
    parent = {}
    queue = Queue()

    for node in G:
        visited[node] = False
        parent[node] = None

    queue.put(maze.start_j)
    visited[maze.start_j] = True

    # bfs
    while not queue.empty():
        u = queue.get()

        for v in G.neighbors(u):
            if not visited[v]:
                visited[v] = True
                parent[v] = u
                queue.put(v)

    # creating path from O to X
    v = X
    while v is not None:
        if parent[v] is not None:
            if v - parent[v] == len(maze.list_view[0]):
                path += "D"
            elif v - parent[v] == -len(maze.list_view[0]):
                path += "U"
            elif v - parent[v] == 1:
                path += "R"
            elif v - parent[v] == -1:
                path += "L"
        v = parent[v]

    # flip the path, also remove the last character so that X is displayed in the maze
    path = path[::-1][:-1]

    print(f"Found: {path}")
    maze.print(path)


def _shift_coordinate(i: int, j: int, move: str) -> tuple[int, int]:
    if move == "L":
        j -= 1
    elif move == "R":
        j += 1
    elif move == "U":
        i -= 1
    elif move == "D":
        i += 1
    return i, j


if __name__ == "__main__":
    maze = Maze.from_file("maze_2.txt")
    t_start = perf_counter()
    solve(maze)
    t_end = perf_counter()
    print(f"Elapsed time: {t_end - t_start} sec")
