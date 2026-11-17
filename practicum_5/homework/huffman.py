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
        self.decode_table: dict[str, Any] = {}

    def _build_codes(self, sequence: list[Any]) -> None:
        freqs: dict[Any, int] = {}
        for symbol in sequence:
            freqs[symbol] = freqs.get(symbol, 0) + 1

        heap = [(f, i, ("leaf", sym)) for i, (sym, f) in enumerate(freqs.items())]
        heapq.heapify(heap)
        counter = len(heap)
        while len(heap) > 1:
            f1, _, t1 = heapq.heappop(heap)
            f2, _, t2 = heapq.heappop(heap)
            heapq.heappush(heap, (f1 + f2, counter, ("node", t1, t2)))
            counter += 1

        self.codes = {}
        if heap:
            root = heap[0][2]
            if root[0] == "leaf":
                self.codes[root[1]] = "0"
            else:
                stack = [(root, "")]
                while stack:
                    tree, prefix = stack.pop()
                    if tree[0] == "leaf":
                        self.codes[tree[1]] = prefix
                    else:
                        stack.append((tree[1], prefix + "0"))
                        stack.append((tree[2], prefix + "1"))
        self.decode_table = {code: sym for sym, code in self.codes.items()}

    def encode(self, sequence: list[Any]) -> str:
        sequence = list(sequence)
        self._build_codes(sequence)
        return "".join(self.codes[symbol] for symbol in sequence)

    def decode(self, encoded_sequence: str) -> list[Any]:
        decoded = []
        current = ""
        for bit in encoded_sequence:
            current += bit
            if current in self.decode_table:
                decoded.append(self.decode_table[current])
                current = ""
        return decoded


class LossyCompression:
    def __init__(self, n_levels: int = 64) -> None:
        self.n_levels = n_levels
        self.huffman = HuffmanCoding()
        self.z_min = 0.0
        self.z_max = 1.0

    def compress(self, time_series: NDArrayFloat) -> str:
        self.z_min = float(np.min(time_series))
        self.z_max = float(np.max(time_series))
        width = (self.z_max - self.z_min) / self.n_levels
        if width == 0:
            indices = np.zeros(len(time_series), dtype=int)
        else:
            indices = np.floor((time_series - self.z_min) / width).astype(int)
            indices = np.clip(indices, 0, self.n_levels - 1)
        return self.huffman.encode(indices.tolist())

    def decompress(self, bits: str) -> NDArrayFloat:
        indices = np.array(self.huffman.decode(bits), dtype=float)
        width = (self.z_max - self.z_min) / self.n_levels
        return self.z_min + (indices + 0.5) * width


if __name__ == "__main__":
    ts = np.loadtxt("ts_homework_practicum_5.txt")

    compressor = LossyCompression()
    bits = compressor.compress(ts)
    decompressed_ts = compressor.decompress(bits)

    compression_ratio = (len(ts) * 32 * 8) / len(bits) 
    print(f"Compression ratio: {compression_ratio:.2f}")

    compression_loss = np.sqrt(np.mean((ts - decompressed_ts)**2))
    print(f"Compression loss (RMSE): {compression_loss}")

