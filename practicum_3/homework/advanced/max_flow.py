from typing import Any

import networkx as nx

def bfs(G, s, t, parent):
	visited = [False] * len(G.nodes())
	visited[s] = True
	quene = set()
	quene.add(s)
	while quene:
		cur = int(quene.pop())
		for neighbor in G.neighbors(str(cur)):
			if visited[int(neighbor)] == False:
				visited[int(neighbor)] = True
				parent[int(neighbor)] = cur
				quene.add(neighbor)
	return visited[t]
	

def max_flow(G: nx.Graph, s: Any, t: Any) -> int:
	value: int = 0
	parent = [-1] * len(G.nodes())
	while bfs(G, s, t, parent):
		cur_flow = 999999
		end = t
		while end != s:
			cur_flow = min(cur_flow, G.get_edge_data(str(parent[end]), str(end))['weight'])
			end = parent[end]
		value += cur_flow
		end = t
		while end != s:
			G[str(parent[end])][str(end)]['weight'] -= cur_flow
			if (G[str(parent[end])][str(end)]['weight'] == 0):
				G.remove_edge(str(parent[end]), str(end))
			nx.add_path(G, [str(end), str(parent[end])], weight = 0)
			G[str(end)][str(parent[end])]['weight'] += cur_flow
			end = parent[end]
	return value 


if __name__ == "__main__":
	# Load the graph
	G = nx.read_edgelist("practicum_3/homework/advanced/graph_1.edgelist", create_using=nx.DiGraph)
	val = max_flow(G, s=0, t=5)
	print(f"Maximum flow is {val}. Should be 23")
