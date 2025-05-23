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
        self.codes = {}
        self.reverse_codes = {}

    def encode(self, sequence: list[Any]) -> str:
        freq = {}
        for s in sequence:
            freq[s] = freq.get(s, 0) + 1
        heap = [[f, [sym, ""]] for sym, f in freq.items()]
        import heapq
        heapq.heapify(heap)
        while len(heap) > 1:
            lo = heapq.heappop(heap)
            hi = heapq.heappop(heap)
            for pair in lo[1:]:
                pair[1] = '0' + pair[1]
            for pair in hi[1:]:
                pair[1] = '1' + pair[1]
            heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
        huff_pairs = heap[0][1:]
        self.codes = {sym: code for sym, code in huff_pairs}
        self.reverse_codes = {code: sym for sym, code in huff_pairs}
        return ''.join(self.codes[s] for s in sequence)

    def decode(self, encoded_sequence: str) -> list[Any]:
        result = []
        code = ""
        for bit in encoded_sequence:
            code += bit
            if code in self.reverse_codes:
                result.append(self.reverse_codes[code])
                code = ""
        return result

class LossyCompression:
    def __init__(self, K: int = 256) -> None:
        self.K = K
        self.huffman = HuffmanCoding()
        self.centers = None
        self.bins = None

    def compress(self, time_series: NDArrayFloat) -> str:
        x = time_series
        min_x, max_x = np.min(x), np.max(x)
        self.bins = np.linspace(min_x, max_x, self.K + 1)
        self.centers = (self.bins[:-1] + self.bins[1:]) / 2
        inds = np.digitize(x, self.bins) - 1
        inds[inds == self.K] = self.K - 1
        inds = inds.tolist()
        return self.huffman.encode(inds)

    def decompress(self, bits: str) -> NDArrayFloat:
        inds = self.huffman.decode(bits)
        inds = np.array(inds, dtype=int)
        return self.centers[inds]

if __name__ == "__main__":
    ts = np.loadtxt("ts_homework_practicum_5.txt")

    compressor = LossyCompression()
    bits = compressor.compress(ts)
    decompressed_ts = compressor.decompress(bits)

    compression_ratio = (len(ts) * 32 * 8) / len(bits) 
    print(f"Compression ratio: {compression_ratio:.2f}")

    compression_loss = np.sqrt(np.mean((ts - decompressed_ts)**2))
    print(f"Compression loss (RMSE): {compression_loss}")

