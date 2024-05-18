from typing import Any

import networkx as nx

def dfs_check_path(G:nx.DiGraph, start_node:str, target_node:str, parent:dict[str, str]) -> bool:
    """
    return True, if there is a path from start_node to target_node
    fill dict parent with key:value = node:one of node parents 
    """
    visited = set()
    stack = set()
    stack.add(start_node)

    while stack:
        node = stack.pop()

        if node in visited:
            continue

        visited.add(node)

        for neighbor in G.neighbors(node):
            if neighbor not in visited:
                parent[neighbor] = node
                stack.add(neighbor)

    return target_node in visited



def max_flow(G:nx.DiGraph, s:Any, t:Any) -> int:
    s = str(s)
    t = str(t)
    result = 0
    parent = dict()
    for node in G.nodes():
        parent[node] = None
    
    while dfs_check_path(G, s, t, parent):
        path_flow = float("Inf")
        current_node = t

        while (current_node != s):
            current_parent = parent[current_node]
            path_flow = min(path_flow, G.get_edge_data(current_parent, current_node)["weight"]) 
            current_node = current_parent

        result += path_flow
        
        current_node = t
        while (current_node != s):
            current_parent = parent[current_node]
            G[current_parent][current_node]["weight"] -= path_flow
            if (G[current_parent][current_node]["weight"] == 0):
                G.remove_edge(current_parent, current_node)
            G.add_edge(current_node, current_parent, weight=path_flow)
            current_node = current_parent
        
    return int(result)


if __name__ == "__main__":
    # Load the graph
    G = nx.read_edgelist("practicum_3/homework/advanced/graph_1.edgelist", create_using=nx.DiGraph)
    val = max_flow(G, s=0, t=5)
    print(f"Maximum flow is {val}. Should be 23")
