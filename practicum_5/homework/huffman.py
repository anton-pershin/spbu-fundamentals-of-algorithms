import sys
from pathlib import Path

project_root = Path("C:/IT/code/spbu-fundamentals-of-algorithms")
sys.path.insert(0, str(project_root))

import heapq
from typing import Any
from abc import ABC, abstractmethod
from sys import getsizeof

import networkx as nx
import numpy as np

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph, NDArrayFloat


class HuffmanCoding:
    def __init__(self) -> None:
        self.codes = {}
        self.reverse_codes = {}

    def encode(self, data: list[Any]) -> str:
        counts = {}
        for x in data:
            counts[x] = counts.get(x, 0) + 1

        heap = [(freq, sym) for sym, freq in counts.items()]
        heapq.heapify(heap)

        if len(heap) == 1:
            _, sym = heap[0]
            self.codes = {sym: "0"}
            self.reverse_codes = {"0": sym}
        else:
            while len(heap) > 1:
                f1, left = heapq.heappop(heap)
                f2, right = heapq.heappop(heap)
                heapq.heappush(heap, (f1 + f2, (left, right)))

            self.codes.clear()
            self.reverse_codes.clear()
            stack = [("", heap[0][1])]

            while stack:
                prefix, node = stack.pop()
                if isinstance(node, tuple):
                    left, right = node
                    stack.append((prefix + "0", left))
                    stack.append((prefix + "1", right))
                else:
                    code = prefix or "0"
                    self.codes[node] = code
                    self.reverse_codes[code] = node

        return "".join(self.codes[x] for x in data)

    def decode(self, encoded_sequence: str) -> list[Any]:
        result = []
        current = ""
        for bit in encoded_sequence:
            current += bit
            if current in self.reverse_codes:
                result.append(self.reverse_codes[current])
                current = ""
        return result


class LossyCompression:
    def __init__(self):
        self.min = None
        self.max = None
        self.bits = 4
        self.huffman = HuffmanCoding()

    def compress(self, time_series: NDArrayFloat) -> str:
        self.min = np.min(time_series)
        self.max = np.max(time_series)
        quantized = [
            int(((x - self.min) / (self.max - self.min)) * (2**self.bits - 1))
            for x in time_series
        ]
        return self.huffman.encode(quantized)

    def decompress(self, bits: str) -> NDArrayFloat:
        quantized = np.array(self.huffman.decode(bits), dtype=np.float32)
        normalized = quantized / (2**self.bits - 1)
        return normalized * (self.max - self.min) + self.min


if __name__ == "__main__":
    ts_path = project_root / "practicum_5" / "homework" / "ts_homework_practicum_5.txt"
    ts = np.loadtxt(ts_path)

    compressor = LossyCompression()
    bits = compressor.compress(ts)
    decompressed_ts = compressor.decompress(bits)

    compression_ratio = (len(ts) * 32 * 8) / len(bits)
    print(f"Compression ratio: {compression_ratio:.2f}")

    compression_loss = np.sqrt(np.mean((ts - decompressed_ts) ** 2))
    print(f"Compression loss (RMSE): {compression_loss}")
