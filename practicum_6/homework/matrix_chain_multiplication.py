from pathlib import Path
from typing import Any, Union

import numpy as np
import networkx as nx

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class MatrixChainMultiplication:
    def __init__(self) -> None:
        self.cnt = 0
        

    def run(
        self,
        matrices: list[dict[str, Union[str, tuple[int, int]]]]
    ) -> tuple[AnyNxGraph, Any]:
        sz = len(matrices)
        
        if sz == 0:
            return nx.Graph(), None
        if sz == 1:
            g = nx.Graph()
            leaf_id = matrices[0]["matrix_name"]
            g.add_node(leaf_id)
            return g, leaf_id

        dims = [matrices[0]["shape"][0]] + [m["shape"][1] for m in matrices]

        opt = np.zeros((sz, sz))
        cut = np.zeros((sz, sz), dtype=int)

        for ln in range(2, sz + 1):
            for l in range(sz - ln + 1):
                r = l + ln - 1
                opt[l, r] = float('inf')
                for md in range(l, r):
                    val = opt[l, md] + opt[md + 1, r] + dims[l] * dims[md + 1] * dims[r + 1]
                    if val < opt[l, r]:
                        opt[l, r] = val
                        cut[l, r] = md

        G = nx.Graph()
        self.cnt = 0

        def dfs(l: int, r: int) -> str:
            if l == r:
                node_name = matrices[l]["matrix_name"]
                G.add_node(node_name)
                return node_name

            mid = cut[l, r]

            left_res = dfs(l, mid)
            right_res = dfs(mid + 1, r)

            self.cnt += 1
            new_node = f"Node_{self.cnt}"

            G.add_node(new_node)
            G.add_edge(new_node, left_res)
            G.add_edge(new_node, right_res)

            return new_node

        root = dfs(0, sz - 1)

        return G, root
        


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

