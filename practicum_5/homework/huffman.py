from pathlib import Path
import heapq
from typing import Any
from abc import ABC, abstractmethod
from itertools import count

import networkx as nx
import numpy as np

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph, NDArrayFloat

class HuffmanCoding:
    def __init__(self):
        self.codes = {}
        self.reverse_codes = {}
        self.root = None
        self._counter = count()

    def encode(self, sequence):
        if not sequence:
            return ""
        freq = {}
        for c in sequence:
            freq[c] = freq.get(c, 0) + 1
        heap = [(f, next(self._counter), c, None, None) for c, f in freq.items()]
        heapq.heapify(heap)
        while len(heap) > 1:
            f1, _, c1, l1, r1 = heapq.heappop(heap)
            f2, _, c2, l2, r2 = heapq.heappop(heap)
            merged = (f1 + f2, next(self._counter), None,
                      (f1, None, c1, l1, r1),
                      (f2, None, c2, l2, r2))
            heapq.heappush(heap, merged)
        self.root = heap[0] if heap else None
        self.codes.clear()
        self.reverse_codes.clear()
        def _gen(node, prefix=""):
            if not node:
                return
            _, _, ch, left, right = node
            if ch is not None:
                self.codes[ch] = prefix
                self.reverse_codes[prefix] = ch
            else:
                _gen(left, prefix + "0")
                _gen(right, prefix + "1")
        _gen(self.root)
        return "".join(self.codes[c] for c in sequence)

    def decode(self, encoded_str):
        if not encoded_str or self.root is None:
            return []
        result = []
        node = self.root
        for bit in encoded_str:
            node = node[3] if bit == '0' else node[4]
            if node[2] is not None:
                result.append(node[2])
                node = self.root
        return result



class LossyCompression:
    def __init__(self, scale: int = 10): 
        self.scale = scale
        self.huffman = HuffmanCoding()

    def compress(self, time_series: NDArrayFloat) -> str:
        scaled = np.round(time_series * self.scale).astype(int)
        return self.huffman.encode(scaled.tolist())

    def decompress(self, bits: str) -> NDArrayFloat:
        decoded = self.huffman.decode(bits)
        return np.array(decoded, dtype=float) / self.scale


if __name__ == "__main__":
    ts = np.loadtxt("ts_homework_practicum_5.txt")

    compressor = LossyCompression()
    bits = compressor.compress(ts)
    decompressed_ts = compressor.decompress(bits)

    compression_ratio = (len(ts) * 32 * 8) / len(bits) 
    print(f"Compression ratio: {compression_ratio:.2f}")

    compression_loss = np.sqrt(np.mean((ts - decompressed_ts)**2))
    print(f"Compression loss (RMSE): {compression_loss}")
