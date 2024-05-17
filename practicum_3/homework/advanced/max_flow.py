from typing import Any
import math
from src.plotting import plot_graph
import networkx as nx
import numpy as np

# Breath first search
def bfs(G, s, t, parent): 
    visited = [False] * len(G.nodes())
    queue = set()
    
    visited[int(s)] = True
    queue.add(s)
    while queue: 
        node = int(queue.pop())
        for neighbour in G.neighbors(str(node)): 
            if not visited[int(neighbour)]: 
                visited[int(neighbour)] = True
                parent[int(neighbour)] = node
                queue.add(neighbour)
    return visited[t]  # If we visited our GOAL node then we will return True
                
# Our main function
def max_flow(G: nx.Graph, s: Any, t: Any) -> int:
    value: int = 0
    parent = [-1] * len(G.nodes()) # Array of parents, shows us a node, from which we came
    
    while bfs(G, s, t, parent): # While we can reach our GOAL node
        tmp_flow = math.inf
        end = t
        # Find min edge from all the edges, that are in path
        while (end != s):
            tmp_flow = min(tmp_flow, G.get_edge_data(str(parent[end]), str(end))["weight"]) 
            end = parent[end]
            
        value += tmp_flow
        
        end = t
        while (end != s):
            G[str(parent[end])][str(end)]['weight'] -= tmp_flow # Decrease our edges
            if (G[str(parent[end])][str(end)]['weight'] == 0): # Remove them if they are zero
                G.remove_edge(str(parent[end]), str(end))
            nx.add_path(G, [str(end), str(parent[end])], weight = 0) # Create reverse one
            G[str(end)][str(parent[end])]['weight'] += tmp_flow # Increase our new edges
            end = parent[end]
        
    return value


if __name__ == "__main__":
    # Load the graph
    G = nx.read_edgelist("practicum_3/homework/advanced/graph_1.edgelist", create_using=nx.DiGraph)
    #plot_graph(G)
    val = max_flow(G, s=0, t=5)
    print(f"Maximum flow is {val}. Should be 23")