import sys
from pathlib import Path
from typing import Any

import numpy as np
import networkx as nx
from scipy.optimize import milp, Bounds, LinearConstraint

if __name__ == "__main__" and not __package__:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph, NDArrayInt, NDArrayFloat


class TSPIntegerLinearProgram:
    def __init__(self, G: AnyNxGraph) -> None:

        self.G = G
        self.nodes: list[Any] = list(G.nodes)
        self.adj_matrix = nx.to_numpy_array(G, nodelist=self.nodes, weight="weight")

    def solve(self, start_node: Any) -> set[tuple[Any, Any]]:

        n = len(self.nodes)
        s_i = self.nodes.index(start_node)
        edge_idx_map = self.build_edge_idx_map(self.adj_matrix)
        n_edges = len(edge_idx_map)
        n_vars = n_edges + n

        c = np.zeros(n_vars)
        for (i, j), k in edge_idx_map.items():
            c[k] = self.adj_matrix[i, j]

        constraints = []

        A_deg = np.zeros((2 * n, n_vars))
        for (i, j), k in edge_idx_map.items():
            A_deg[i, k] = 1
            A_deg[n + j, k] = 1
        constraints.append(LinearConstraint(A_deg, lb=1, ub=1))

        rows = []
        for (i, j), k in edge_idx_map.items():
            if i == s_i or j == s_i:
                continue
            row = np.zeros(n_vars)
            row[n_edges + i] = 1
            row[n_edges + j] = -1
            row[k] = n - 1
            rows.append(row)
        if rows:
            constraints.append(LinearConstraint(np.array(rows), lb=-np.inf, ub=n - 2))

        lb = np.concatenate([np.zeros(n_edges), np.full(n, 2.0)])
        ub = np.concatenate([np.ones(n_edges), np.full(n, float(n))])
        lb[n_edges + s_i] = ub[n_edges + s_i] = 1.0

        res = milp(
            c,
            constraints=constraints,
            integrality=np.ones(n_vars),
            bounds=Bounds(lb, ub),
        )
        if not res.success:
            raise ValueError("No Hamiltonian cycle found")

        return {
            (self.nodes[i], self.nodes[j])
            for (i, j), k in edge_idx_map.items()
            if res.x[k] > 0.5
        }

    @staticmethod
    def build_edge_idx_map(adj_matrix: NDArrayInt | NDArrayFloat) -> dict[tuple[int, int], int]:
        edge_idx_map = {}
        edge_idx = 0
        for i in range(adj_matrix.shape[0]):
            for j in range(adj_matrix.shape[1]):
                if adj_matrix[i, j] != 0:
                    edge_idx_map[(i, j)] = edge_idx
                    edge_idx += 1
        return edge_idx_map


if __name__ == "__main__":
    G = nx.complete_graph(5, create_using=nx.DiGraph)
    for u, v in G.edges():
        G.edges[u, v]["weight"] = np.random.randint(1, 20)
    plot_graph(G)

    start_node = 0
    ilp = TSPIntegerLinearProgram(G)
    tour_edges = ilp.solve(start_node=start_node)
    plot_graph(G, highlighted_edges=list(tour_edges))
    print(tour_edges)
