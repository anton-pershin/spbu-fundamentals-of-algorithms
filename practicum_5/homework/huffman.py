from pathlib import Path
import heapq
from typing import Any
from abc import ABC, abstractmethod

import networkx as nx
import numpy as np

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph, NDArrayFloat


class Node:
    def __init__(self, freq: float, symbol: Any = None, left: "Node" = None, right: "Node" = None) -> None:
        self.freq = freq
        self.symbol = symbol
        self.left = left
        self.right = right

    def __lt__(self, other: "Node") -> bool:
        return self.freq < other.freq


class HuffmanCoding:
    def __init__(self) -> None:
        self.root: Node | None = None

    def _build_tree(self, sequence: list[Any]) -> None:
        freq: dict[Any, int] = {}
        for s in sequence:
            freq[s] = freq.get(s, 0) + 1

        heap = [Node(f, symbol=s) for s, f in freq.items()]
        heapq.heapify(heap)

        # Крайний случай: в последовательности всего один уникальный символ
        if len(heap) == 1:
            only = heapq.heappop(heap)
            heapq.heappush(heap, Node(only.freq, left=only, right=None))

        while len(heap) > 1:
            a = heapq.heappop(heap)
            b = heapq.heappop(heap)
            parent = Node(a.freq + b.freq, left=a, right=b)
            heapq.heappush(heap, parent)

        self.root = heap[0]

    def _build_codes(self, node: Node, prefix: str, codes: dict[Any, str]) -> None:
        if node is None:
            return
        if node.symbol is not None:
            codes[node.symbol] = prefix if prefix else "0"
            return
        self._build_codes(node.left, prefix + "0", codes)
        self._build_codes(node.right, prefix + "1", codes)

    def encode(self, sequence: list[Any]) -> str:
        self._build_tree(sequence)
        codes: dict[Any, str] = {}
        self._build_codes(self.root, "", codes)
        return "".join(codes[s] for s in sequence)

    def decode(self, encoded_sequence: str) -> list[Any]:
        result = []
        node = self.root
        for bit in encoded_sequence:
            node = node.left if bit == "0" else node.right
            if node.symbol is not None:
                result.append(node.symbol)
                node = self.root
        return result


class LossyCompression:
    def __init__(self, n_levels: int = 256) -> None:
        self.n_levels = n_levels
        self.huffman = HuffmanCoding()
        self.centers: NDArrayFloat | None = None

    def _quantize(self, time_series: NDArrayFloat) -> np.ndarray:
        z_min = time_series.min()
        z_max = time_series.max()
        edges = np.linspace(z_min, z_max, self.n_levels + 1)
        self.centers = (edges[:-1] + edges[1:]) / 2
        indices = np.digitize(time_series, edges[1:-1])
        indices = np.clip(indices, 0, self.n_levels - 1)
        return indices

    def compress(self, time_series: NDArrayFloat) -> str:
        indices = self._quantize(time_series)
        return self.huffman.encode(indices.tolist())

    def decompress(self, bits: str) -> NDArrayFloat:
        indices = self.huffman.decode(bits)
        return np.array([self.centers[i] for i in indices])


if __name__ == "__main__":
    ts = np.loadtxt("ts_homework_practicum_5.txt")
    compressor = LossyCompression()
    bits = compressor.compress(ts)
    decompressed_ts = compressor.decompress(bits)
    compression_ratio = (len(ts) * 32 * 8) / len(bits)
    print(f"Compression ratio: {compression_ratio:.2f}")
    compression_loss = np.sqrt(np.mean((ts - decompressed_ts)**2))
    print(f"Compression loss (RMSE): {compression_loss}")
