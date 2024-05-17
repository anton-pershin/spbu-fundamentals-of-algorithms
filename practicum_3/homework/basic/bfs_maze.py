from time import perf_counter
import numpy as np

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
    m = np.zeros((len(maze.list_view), len(maze.list_view)))
    m[0, maze.start_j] = 1


    end_j = 0
    for j, sym in enumerate(maze.list_view[-1]):
        if sym == "X":
            end_j = j
    print(end_j)

    def make_step(k):
        for i in range(len(m)):
            for j in range(len(m[i])):
                if m[i][j] == k:
                    if i>0 and m[i-1][j] == 0 and maze.list_view[i-1][j] == ' ':
                        m[i-1][j] = k + 1
                    if j>0 and m[i][j-1] == 0 and maze.list_view[i][j-1] == ' ':
                        m[i][j-1] = k + 1
                    if i<len(m)-1 and m[i+1][j] == 0 and maze.list_view[i+1][j] == ' ':
                        m[i+1][j] = k + 1
                    if j<len(m[i])-1 and m[i][j+1] == 0 and maze.list_view[i][j+1] == ' ':
                        m[i][j+1] = k + 1
    k = 1
    while m[len(m) - 2, end_j] == 0:
        make_step(k)
        k += 1

    i, j = (len(m) - 2), end_j
    k = m[i][j]
    path += 'D'
    while k > 1:
        if i > 0 and m[i - 1][j] == k-1:
            i, j = i-1, j
            path += 'D'
            k-=1
        elif j > 0 and m[i][j - 1] == k-1:
            i, j = i, j-1
            path += 'R'
            k-=1
        elif i < len(m) - 1 and m[i + 1][j] == k-1:
            i, j = i+1, j
            path += 'U'
            k-=1
        elif j < len(m[i]) - 1 and m[i][j + 1] == k-1:
            i, j = i, j+1
            path += 'L'
            k -= 1

    path = path[::-1]
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
    maze = Maze.from_file("practicum_3/homework/basic/maze_2.txt")
    t_start = perf_counter()
    solve(maze)
    t_end = perf_counter()
    print(f"Elapsed time: {t_end - t_start} sec")
