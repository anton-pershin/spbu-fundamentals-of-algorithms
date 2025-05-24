from pathlib import Path
from typing import Any, Union
import numpy as np
import networkx as nx
import sys
sys.path.append(r"/Users/alexanderkuka/documents/python/pershin/spbu-fundamentals-of-algorithms")

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class MatrixChainMultiplication:
    def __init__(self) -> None:
        pass

    def run(self, matrices: list[dict[str, Union[str, tuple[int, int]]]]) -> tuple[AnyNxGraph, Any]:
        
        n = len(matrices)
        dims = [matrices[0]["shape"][0]] + [m["shape"][1] for m in matrices]

        cost = np.zeros((n, n))
        split = np.zeros((n, n), dtype=int)

        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                cost[i][j] = float('inf')
                
                for k in range(i, j):
                    current_cost = cost[i][k] + cost[k+1][j] + dims[i] * dims[k+1] * dims[j+1]
                    if current_cost < cost[i][j]:
                        cost[i][j] = current_cost
                        split[i][j] = k

        graph = nx.DiGraph()
        node_id = 0

        def make_tree(i, j):
            nonlocal node_id
            
            if i == j:
                name = matrices[i]["matrix_name"]
                graph.add_node(name)
                return name
            
            k = split[i][j]
            internal_name = f"node_{node_id}"
            node_id += 1
            
            graph.add_node(internal_name)
            left = make_tree(i, k)
            right = make_tree(k+1, j)
            
            graph.add_edge(internal_name, left)
            graph.add_edge(internal_name, right)
            
            return internal_name

        root = make_tree(0, n-1)
        return graph, root

if __name__ == "__main__":
    test_matrices = [
        {
            "matrix_name": "A",
            "shape": (2, 3),
        },
        {
            "matrix_name": "B",
            "shape": (3, 10),
        },
        {
            "matrix_name": "C",
            "shape": (10, 20),
        },
        {
            "matrix_name": "D",
            "shape": (20, 3),
        },
    ]
    
    mcm = MatrixChainMultiplication()
    matmul_tree, root = mcm.run(test_matrices)
    plot_graph(matmul_tree)

