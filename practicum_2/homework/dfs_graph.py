from pathlib import Path
print('Running' if __name__ == '__main__' else 'Importing', Path(__file__).resolve())

import queue
from typing import Any, Callable
import time
import sys

import networkx as nx

from src.plotting import plot_graph

def dfs_iterative(G: nx.Graph, start:Any, log=True) -> list:
	if log: print(f"[{time.ctime(time.time())[11:19]}]Starting DFS[I]")
	visited = {node: False for node in G}; visited[start] = True
	result = [start]; temps = [start]
	
	while temps:
		start = temps[-1]
		if not visited[start]:
			result += [start]
			visited[start] = True
			if log: print("\t\t visiting", start)
		
		for next in G.neighbors(start):
			if not visited[next]:
				temps += [next]
				if log: print("\t\t visiting", start)
				break
		else: temps.pop()
		
	return result
			
		
	
	
def dfs_recursive(G: nx.Graph, start: Any, visited=None, result=None, log=True) -> list:
	if result is None:
		if log: print(f"[{time.ctime(time.time())[11:19]}]Starting DFS[R]")
		result = []
	if visited is None:
		visited = {node: False for node in G}
		
	if not visited[start]:
		visited[start] = True
		result += [start]
		
		if log: print("\t\t visiting", start)
	else:
		return result;
	
	for next in G.neighbors(start):
		result = dfs_recursive(G, next, visited, result, log)
	
	return result


def topological_sort(G: nx.DiGraph, log=True):
	if log: print(f"[{time.ctime(time.time())[11:19]}]Starting TS")
	
	indegrees = {n: d for n, d in G.in_degree() if d > 0}
	zero_indegrees = [n for n, d in G.in_degree() if d == 0]
	
	result = []
	while zero_indegrees:
		tmp = zero_indegrees
		zero_indegrees = []
		
		for start in tmp:
			for next in G.neighbors(start):
				indegrees[next] -= 1
				if indegrees[next] == 0:
					zero_indegrees += [next]
					del indegrees[next]
		
		result += tmp
	return result
    

def assert_algo(algo_to_check: Callable, algo_true: Callable, *options) -> bool:
	return (algo_to_check(*options) == algo_true(*options))


if __name__ == "__main__":
    # Load and plot the graph
    G = nx.read_edgelist("homework/graph_2.edgelist", create_using=nx.Graph)
	
    print("Recursive DFS")
    print("-" * 32)
    #print("DFS for start=0:", assert_algo(lambda x: dfs_recursive(x, start="0", log=False), lambda x: [n for n in nx.dfs_tree(x)], G))
    #print(dfs_recursive(G, start="0"))
    print()
    
    print("Iterative DFS")
    print("-" * 32)
    print("DFS for start=0:", assert_algo(lambda x: dfs_iterative(x, start="0", log=False), lambda x: [n for n in nx.dfs_tree(x)], G))
    print(dfs_iterative(G, start="0"))
    print()
    
    
    plot_graph(G)
    G = nx.read_edgelist("homework/graph_2.edgelist", create_using=nx.DiGraph)
    
    print("Topological sort")
    print("-" * 32)
    #print("TS:", assert_algo(topological_sort, lambda x: [n for n in nx.topological_sort(x)], G))
    print(topological_sort(G))
    print()
    
    plot_graph(G)
