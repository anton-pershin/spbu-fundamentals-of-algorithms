from collections import Counter
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

    def _build_tree(self, frequencies):
        heap = []
        counter = 0

        for symbol, freq in frequencies.items():
            heapq.heappush(heap, (freq, counter, symbol, None, None))
            counter += 1

        while len(heap) > 1:
            freq1, cnt1, sym1, left1, right1 = heapq.heappop(heap)
            freq2, cnt2, sym2, left2, right2 = heapq.heappop(heap)

            parent_freq = freq1 + freq2
            heapq.heappush(heap, (parent_freq, counter, None,
                                  (freq1, cnt1, sym1, left1, right1),
                                  (freq2, cnt2, sym2, left2, right2)))
            counter += 1

        return heap[0] if heap else None

    def _generate_codes(self, node, code="") -> None:
        if node is None:
            return

        freq, counter, symbol, left, right = node

        if symbol is not None:
            self.codes[symbol] = code
            self.reverse_codes[code] = symbol
        else:
            self._generate_codes(left, code + "0")
            self._generate_codes(right, code + "1")

    def encode(self, sequence: list[Any]) -> str:
        if not sequence:
            return ""

        frequencies = Counter(sequence)
        root = self._build_tree(frequencies)
        self.codes.clear()
        self.reverse_codes.clear()

        if root:
            self._generate_codes(root)

        return "".join(self.codes[symbol] for symbol in sequence)


    def decode(self, encoded_sequence: str) -> list[Any]:
        if not encoded_sequence or not self.reverse_codes:
            return []

        decoded = []
        current_code = ""

        for bit in encoded_sequence:
            current_code += bit
            if current_code in self.reverse_codes:
                decoded.append(self.reverse_codes[current_code])
                current_code = ""

        return decoded


class LossyCompression:
    def __init__(self, K: int = 10) -> None:
        self.K = K
        self.bins = None
        self.centers = None
        self.huffman = None

    def _quantize(self, value: float) -> float:
        for i in range(len(self.bins) - 1):
            if self.bins[i] <= value <= self.bins[i + 1]:
                return self.centers[i]

        if value >= self.bins[-1]:
            return self.centers[-1]

        return self.centers[0]

    def compress(self, time_series: NDArrayFloat) -> str:
        min_val = np.min(time_series)
        max_val = np.max(time_series)
        step = (max_val - min_val) / self.K
        self.bins = np.array([min_val + i * step for i in range(self.K + 1)])
        self.centers = (self.bins[:-1] + self.bins[1:]) / 2

        quan = [self._quantize(x) for x in time_series]
        self.huffman = HuffmanCoding()
        return self.huffman.encode(quan)

    def decompress(self, bits: str) -> NDArrayFloat:
        quan = self.huffman.decode(bits)
        return np.array(quan)


if __name__ == "__main__":
    ts = np.loadtxt("ts_homework_practicum_5.txt")

    compressor = LossyCompression()
    bits = compressor.compress(ts)
    decompressed_ts = compressor.decompress(bits)

    compression_ratio = (len(ts) * 32 * 8) / len(bits) 
    print(f"Compression ratio: {compression_ratio:.2f}")

    compression_loss = np.sqrt(np.mean((ts - decompressed_ts)**2))
    print(f"Compression loss (RMSE): {compression_loss}")