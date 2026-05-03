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
        self.root = None

    def encode(self, sequence: list[Any]) -> str:
        from collections import Counter
        frequencies = Counter(sequence)

        heap = []
        counter = 0
        for symbol, freq in frequencies.items():
            heapq.heappush(heap, (freq, counter, symbol))
            counter += 1
        while len(heap) > 1:
            freq1, _, sym1 = heapq.heappop(heap) 
            freq2, _, sym2 = heapq.heappop(heap) 
            combined = (sym1, sym2)
            heapq.heappush(heap, (freq1 + freq2, counter, combined))
            counter += 1

        self.root = heap[0][2]
        self.codes = {}
        self.reverse_codes = {}
        self._gen_codes(self.root, "")

        encode_str = "".join(self.codes[symbol] for symbol in sequence)
        return encode_str

    def _gen_codes(self, node, current_code):
        if isinstance(node, tuple):
            self._gen_codes(node[0], current_code + "0")
            self._gen_codes(node[1], current_code + "1")
        else:
            self.codes[node] = current_code
            self.reverse_codes[current_code] = node
    

    def decode(self, encoded_sequence: str) -> list[Any]:
        decoded = []
        current_node = self.root

        for bit in encoded_sequence:
            if bit == "0":
                current_node = current_node[0]
            else:
                current_node = current_node[1]
            
            if not isinstance(current_node, tuple):
                decoded.append(current_node)
                current_node = self.root

        return decoded


class LossyCompression:
    def __init__(self) -> None:
        self.K = 64
        self.centers = None
        self.huffman = HuffmanCoding()

    def compress(self, time_series: NDArrayFloat) -> str:
        min_val = np.min(time_series)
        max_val = np.max(time_series)
        
        interval = (max_val - min_val) / self.K
        self.centers = []

        for i in range(self.K):
            left = min_val + i * interval
            right = left + interval
            center = (left + right) / 2
            self.centers.append(center)
        
        indices = []
        for value in time_series:
            idx = int((value - min_val) / interval)
            if idx >= self.K:
                idx = self.K - 1
            if idx < 0:
                idx = 0
            indices.append(idx)
        
        bits = self.huffman.encode(indices)
        return bits

    def decompress(self, bits: str) -> NDArrayFloat:
        indices = self.huffman.decode(bits)
        
        restored = np.array([self.centers[idx] for idx in indices])
        return restored


if __name__ == "__main__":
    ts = np.loadtxt("ts_homework_practicum_5.txt")

    compressor = LossyCompression()
    bits = compressor.compress(ts)
    decompressed_ts = compressor.decompress(bits)

    compression_ratio = (len(ts) * 32 * 8) / len(bits) 
    print(f"Compression ratio: {compression_ratio:.2f}")

    compression_loss = np.sqrt(np.mean((ts - decompressed_ts)**2))
    print(f"Compression loss (RMSE): {compression_loss}")

