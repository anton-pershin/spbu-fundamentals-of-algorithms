from pathlib import Path
import heapq
from typing import Any
from abc import ABC, abstractmethod

import networkx as nx
import numpy as np

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph, NDArrayFloat

class HuffmanCoding:
    def __init__(self) -> None:
        self.codes: dict[Any, str] = {}
        self.reverse: dict[str, Any] = {}

    def encode(self, sequence: list[Any]) -> str:
        freq = {}

        for s in sequence:
            if s in freq:
                freq[s] = freq[s] + 1
            else:
                freq[s] = 1

        counter = 0
        heap = []
        for s, f in freq.items():
            heap.append([f, counter, [s, None, None]])
            counter += 1
        heapq.heapify(heap)

        if len(heap) == 1:
            self.codes = {sequence[0]: "0"}
        else:
            while len(heap) > 1:
                lo = heapq.heappop(heap)
                hi = heapq.heappop(heap)
                node = [lo[0] + hi[0], counter, [None, lo[2], hi[2]]]
                counter += 1
                heapq.heappush(heap, node)

            self.codes = {}

            def walk(node, prefix):
                symbol, left, right = node
                if symbol is not None:
                    self.codes[symbol] = prefix
                    return
                walk(left, prefix + "0")
                walk(right, prefix + "1")

            walk(heap[0][2], "")

        self.reverse = {v: k for k, v in self.codes.items()}
        return "".join(self.codes[s] for s in sequence)

    def decode(self, encoded_sequence: str) -> list[Any]:
        result = []
        buf = ""
        for bit in encoded_sequence:
            buf += bit
            if buf in self.reverse:
                result.append(self.reverse[buf])
                buf = ""
        return result


class LossyCompression:
    def __init__(self, n_bins: int = 64) -> None:
        self.n_bins = n_bins
        self.edges = None
        self.centers = None
        self.huffman = None

    def compress(self, time_series: NDArrayFloat) -> str:
        lo, hi = float(time_series.min()), float(time_series.max())

        self.edges = np.linspace(lo, hi, self.n_bins + 1)
        self.centers = (self.edges[:-1] + self.edges[1:]) / 2

        indices = np.digitize(time_series, self.edges[1:-1]).tolist()

        self.huffman = HuffmanCoding()
        return self.huffman.encode(indices)

    def decompress(self, bits: str) -> NDArrayFloat:
        indices = self.huffman.decode(bits)
        return self.centers[np.array(indices)]


if __name__ == "__main__":
    ts = np.loadtxt("ts_homework_practicum_5.txt")

    compressor = LossyCompression()
    bits = compressor.compress(ts)
    decompressed_ts = compressor.decompress(bits)

    compression_ratio = (len(ts) * 32 * 8) / len(bits)
    print(f"Compression ratio: {compression_ratio:.2f}")

    compression_loss = np.sqrt(np.mean((ts - decompressed_ts) ** 2))
    print(f"Compression loss (RMSE): {compression_loss}")