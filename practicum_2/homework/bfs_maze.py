from time import perf_counter
from queue import Queue
import networkx as nx

class Maze:
    def __init__(self, list_view: list[list[str]]) -> None:
        self.list_view = list_view
        self.start = None
        self.end = None
        for j, row in enumerate(self.list_view):
            for i, elem in enumerate(self.list_view[j]):
            	if elem == "O":
            		self.start = [j, i]
            	if elem == "X":
            		self.end = [j, i];

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
        j = self.start
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

def find_path(maze: Maze, G: nx.Graph):
	visited, olders = {}, {}
	lw = maze.list_view
	src = maze.start[0]*len(lw[0]) + maze.start[1]
	dist = maze.end[0]*len(lw[0]) + maze.end[1]
	#print(src, dist, maze.start, maze.end)
	#print(lw)
	q = Queue(); q.put(src)
	
	for node in G:
		print(node)
		visited[node] = False
		olders[node] = None
	visited[src] = True
	
	while not q.empty():
		start = q.get()
		
		for next in G.neighbors(start):
			if not visited[next]:
				visited[next] = True
				olders[next] = start
				q.put(next)
	
	next = dist
	return_path = "";
	while next:
		if olders[next]:
			# horizontal movement
			if (next - olders[next]) == 1:
				return_path += 'R'
			elif (next - olders[next]) == -1:
				return_path += 'L'
			# vertical movement
			elif (next - olders[next]) == len(lw[0]):
				return_path += 'D'
			elif (next - olders[next]) == -len(lw[0]):
				return_path += 'U'
		next = olders[next]
	
	return return_path[::-1]
	
	
def solve(maze: Maze):
	# creating graph with nodes-elements of the maze
	G = nx.Graph()
	edges = []
	lw = maze.list_view
	for j in range(len(lw)):
		for k in range(len(lw[j])):
			if j > 0 and k > 0 and lw[j][k] in [' ', 'X']:
				if lw[j - 1][k] in [' ', 'O']:
					edges += [( len(lw[0])*(j-1) + k, len(lw[0])*(j) + k )]
				if lw[j][k-1] in [' ']:
					edges += [( len(lw[0])*(j) + k-1, len(lw[0])*(j) + k )]
	G.add_edges_from(edges)
	
	return find_path(maze, G)


if __name__ == "__main__":
    maze = Maze.from_file("practicum_2/maze_2.txt")
    t_start = perf_counter()
    print(solve(maze))
    t_end = perf_counter()
    print(f"Elapsed time: {t_end - t_start} sec")
