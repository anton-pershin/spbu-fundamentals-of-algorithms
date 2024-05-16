from collections import deque
from time import perf_counter

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
    start = (0, maze.start_j)
    end = None
    for i, row in enumerate(maze.list_view):
        for j, sym in enumerate(row):
            if sym == "X":
                end = (i, j)
                break
        if end:
            break

    path = bfs(maze.list_view, start, end)
    print(f"Found: {path}")
    maze.print(path)

def bfs(maze, start, end):
    queue = deque([(start, "")])  # Now the queue contains tuples of (coordinate, path)
    seen = set([start])
    while queue:
        (x, y), path = queue.popleft()
        if (x, y) == end:
            return path
        for move, (x2, y2) in [("U", (x-1, y)), ("D", (x+1, y)), ("L", (x, y-1)), ("R", (x, y+1))]:
            if 0 <= x2 < len(maze) and 0 <= y2 < len(maze[0]) and maze[x2][y2] != '#' and (x2, y2) not in seen:
                queue.append(((x2, y2), path + move))
                seen.add((x2, y2))
    return None

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
    maze = Maze.from_file("practicum_3/homework/basic/maze_2.txt")
    t_start = perf_counter()
    solve(maze)
    t_end = perf_counter()
    print(f"Elapsed time: {t_end - t_start} sec")