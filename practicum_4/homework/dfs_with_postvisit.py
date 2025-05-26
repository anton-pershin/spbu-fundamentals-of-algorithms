from pathlib import Path
from typing import Any
import networkx as nx

from practicum_4.dfs import GraphTraversal
from src.plotting.graphs import plot_graph


class DfsViaLifoQueueWithPostvisit(GraphTraversal):
    def run(self, start: Any) -> None:
        stack = [(start, list(self.G.neighbors(start)), 0)]
        self.previsit(start)
        self.visited.add(start)

        while stack:
            node, neighs, idx = stack[-1]
            if idx < len(neighs):
                stack[-1] = (node, neighs, idx + 1)
                nxt = neighs[idx]
                if nxt not in self.visited:
                    self.previsit(nxt)
                    self.visited.add(nxt)
                    stack.append((nxt, list(self.G.neighbors(nxt)), 0))
            else:
                self.postvisit(node)
                stack.pop()


class DfsViaLifoQueueWithPrinting(DfsViaLifoQueueWithPostvisit):
    def previsit(self, node: Any, **params) -> None:
        print(f"Previait node {node}")

    def postvisit(self, node: Any, **params) -> None:
        print(f"Postvisit node {node}")


if __name__ == "__main__":
    G = nx.read_edgelist(
        Path("practicum_4") / "simple_graph_10_nodes.edgelist",
        create_using=nx.Graph
    )
    plot_graph(G)

    dfs = DfsViaLifoQueueWithPrinting(G)
    dfs.run(start="0")
