from pathlib import Path
from typing import Any
import heapq

import networkx as nx

from practicum_4.dfs import GraphTraversal
from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph


class DijkstraAlgorithm(GraphTraversal):
    def __init__(self, G: AnyNxGraph) -> None:
        self.shortest_paths: dict[Any, list[Any]] = {}
        super().__init__(G)

    def previsit(self, node: Any, **params) -> None:
        self.shortest_paths[node] = params["path"]

    def postvisit(self, node: Any, **params) -> None:
        pass

    def run(self, node: Any) -> None:
        #расст-ия и пути от старт-ой вершины
        dist = {node: 0}
        path = {node: [node]}
        #очередь с приоритетом
        pq = [(0, node)]
        visited = set()

        while pq:
            cur_dist, cur = heapq.heappop(pq)
            if cur in visited:
                continue
            visited.add(cur)
            self.previsit(cur, path=path[cur])

            for nb in self.G.neighbors(cur):
                w = float(self.G[cur][nb].get("weight", 1.0))
                new_dist = cur_dist + w
                if nb not in dist or new_dist < dist[nb]:
                    dist[nb] = new_dist
                    path[nb] = path[cur] + [nb]
                    heapq.heappush(pq, (new_dist, nb))


if __name__ == "__main__":
    G = nx.read_edgelist(
        Path("practicum_4") / "simple_weighted_graph_9_nodes.edgelist",
        create_using=nx.Graph
    )
    plot_graph(G)
    sp = DijkstraAlgorithm(G)
    sp.run("0")
    test = "5"
    edges = [(sp.shortest_paths[test][i], sp.shortest_paths[test][i + 1])
             for i in range(len(sp.shortest_paths[test]) - 1)]
    plot_graph(G, highlighted_edges=edges)
