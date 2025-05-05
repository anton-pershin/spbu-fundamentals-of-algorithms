from pathlib import Path
from collections import deque
from typing import Any
from abc import ABC, abstractmethod

import networkx as nx

import sys
sys.path.append(r"/home/viktoria/algoritms/spbu-fundamentals-of-algorithms")

from practicum_4.dfs import GraphTraversal
from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


from collections import deque
from typing import Any

class DfsViaLifoQueueWithPostvisit(GraphTraversal):
    def __init__(self, graph):
        self.graph = graph
        
    def run(self, node: Any) -> None:
        visited = set()
        stack = deque()
        
        stack.append((node, 'enter'))
        
        while len(stack) != 0: 
            current_node, current_state = stack.pop()
            
            if current_state == 'enter':
                if current_node in visited:
                    continue
                    
                self.previsit(current_node)
                visited.add(current_node)
                stack.append((current_node, 'exit'))
                
                neighbors = list(self.graph.neighbors(current_node))  
                for neighbor in neighbors:
                    if neighbor not in visited:
                        stack.append((neighbor, 'enter'))
                        
            elif current_state == 'exit':
                self.postvisit(current_node)


class DfsViaLifoQueueWithPrinting(DfsViaLifoQueueWithPostvisit):
    def previsit(self, node: Any, **params) -> None:
        print(f"Previsit node {node}")

    def postvisit(self, node: Any, **params) -> None:
        print(f"Postvisit node {node}")


if __name__ == "__main__":
    # Load and plot the graph
    G = nx.read_edgelist(
        Path("practicum_4") / "simple_graph_10_nodes.edgelist",
        create_using=nx.Graph
    )
    plot_graph(G)
    dfs = DfsViaLifoQueueWithPrinting(G)
    dfs.run(node="0")

