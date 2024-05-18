from time import perf_counter
from collections import deque

class Maze:
    def __init__(self, list_view: list[list[str]]) -> None:
        self.list_view = list_view #хранит представление лабиринта в виде двумерного списка
        self.start_j = None # хранит индекс столбца, в котором находится стартовая позиция "O"
        for j, sym in enumerate(self.list_view[0]): # ищем символ "O"
            if sym == "O":
                self.start_j = j #сохраняем индекс столбца j символа "O" в переменной start_j

    @classmethod
    def from_file(cls, filename):
        list_view = []
        with open(filename, "r") as f:
            for l in f.readlines():
                list_view.append(list(l.strip()))
        obj = cls(list_view)
        return obj

    def print(self, path="") -> None:
        # Find the path coordinates - найти координаты пути
        i = 0  # in the (i, j) pair, i is usually reserved for rows and j is reserved for columns
        j = self.start_j
        path_coords = set() #будут храниться координаты, через которые проходит путь
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
        path = ""
        start_i = 0 
        start_j = maze.start_j #начальные координаты i и j

        queue = deque([(start_i, start_j, "")])
        visited = set([(start_i, start_j)]) # проверяем посещали ли мы эту вершину, чтобы не возникало рекурсии

        while queue != 0:
            i, j, path = queue.popleft() #извлекаем первый элемент из очереди queue и распаковываем его в переменные i, j и path.
            if maze.list_view[i][j] == "X": #проверяем, достигли ли мы конечной точки Х
                print(f"Found: {path}")
                maze.print(path)
                return
            for move in ["L", "R", "U", "D"]: #исследуем всевозможные направления движения из текущей позиции
                new_i, new_j = _shift_coordinate(i, j, move)
                if (new_i, new_j) not in visited and maze.list_view[new_i][new_j] != "#":
                    visited.add((new_i, new_j))
                    queue.append((new_i, new_j, path + move))
        print("No path found.") 


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
