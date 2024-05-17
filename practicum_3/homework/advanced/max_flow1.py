from typing import Any
from queue import *
from collections import deque
import networkx as nx
import numpy as np

def max_flow(G: nx.Graph, s: Any, t: Any) -> int:
    value: int = 0
    
    min_flow: int = 0
    queue = deque([[str(s)]])
    flows = deque([[np.inf]])

    while queue:
        current_flows = flows.popleft()
        current_path = queue.popleft()
        current_node = current_path[-1]
        if current_node == str(t):
            min_flow = min(current_flows)
            flag = True
            G1 = G.copy()
            for n in range(0, len(current_path) - 1):
                G[current_path[n]][current_path[n+1]]['weight'] -= min_flow
                if G[current_path[n]][current_path[n+1]]['weight'] < 0:
                    flag = False
                    break
            if flag:
                value += min_flow
            else:
                G = G1          
        else:
            for neighbor in G.neighbors(current_node):
                if neighbor not in current_path:
                    flows.append(current_flows + [G[current_node][neighbor]['weight']])
                    queue.append(current_path + [neighbor])
    return value



if __name__ == "__main__":
    # Load the graph
    G = nx.read_edgelist("practicum_3/homework/advanced/graph_1.edgelist", create_using=nx.DiGraph)
    val = max_flow(G, s='0', t='5')
    print(f"Maximum flow is {val}. Should be 23")
