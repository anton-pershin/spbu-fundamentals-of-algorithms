from pathlib import Path
from typing import Any

import networkx as nx

from practicum_4.dfs import GraphTraversal
from src.plotting.graphs import plot_graph


class DfsViaLifoQueueWithPostvisit(GraphTraversal):
    def run(self, node: Any) -> None:
        self.reset()

        stack = [(node, False)]

        while stack:
            current, is_post = stack.pop()

            if is_post:
                self.postvisit(current)
                continue
            if current in self.visited:
                continue
            self.visited.add(current)
            stack.append((current, True))

            self.previsit(current)

            for neigh in reversed(list(self.G.neighbors(current))):
                if neigh not in self.visited:
                    stack.append((neigh, False))


class DfsViaLifoQueueWithPrinting(DfsViaLifoQueueWithPostvisit):
    def previsit(self, node: Any, **params) -> None:
        print(f"Previsit node {node}")

    def postvisit(self, node: Any, **params) -> None:
        print(f"Postvisit node {node}")


if __name__ == "__main__":
    G = nx.read_edgelist(
        Path("practicum_4") / "simple_graph_10_nodes.edgelist",
        create_using=nx.Graph
    )

    dfs = DfsViaLifoQueueWithPrinting(G)
    dfs.run(node="0")
