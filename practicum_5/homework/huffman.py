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
        self.root = None

    def encode(self, sequence: list[Any]) -> str:
        if not sequence:
            return ""

        freq = {}
        for s in sequence:
            freq[s] = freq.get(s, 0) + 1

        heap = []
        counter = 0
        for symbol, count in freq.items():
            node = {"symbol": symbol, "left": None, "right": None}
            heapq.heappush(heap, (count, counter, node))
            counter += 1

        while len(heap) > 1:
            freq1, _, left_node = heapq.heappop(heap)
            freq2, _, right_node = heapq.heappop(heap)
            parent_node = {"symbol": None, "left": left_node, "right": right_node}
            heapq.heappush(heap, (freq1 + freq2, counter, parent_node))
            counter += 1
        
        self.root = heap[0][2]
        self.codes = {}

        def build_codes(node, curr_code=""):
            if node["symbol"] is not None:
                self.codes[node["symbol"]] = curr_code if curr_code else "0"
                return
            build_codes(node["left"], curr_code + "0")
            build_codes(node["right"], curr_code + "1")

        build_codes(self.root)

        return "".join(self.codes[s] for s in sequence)
    
    def decode(self, encoded_sequence: str) -> list[Any]:

        if not encoded_sequence or not self.root:
            return []

        result = []
        node = self.root
        for bit in encoded_sequence:
            node = node["left"] if bit == "0" else node["right"]
            if node["symbol"] is not None:
                result.append(node["symbol"])
                node = self.root

        return result


class LossyCompression:
    def __init__(self) -> None:

        self.K = 16
        self.huffman = HuffmanCoding()
        self.centers = None
        self.boundaries = None

    def compress(self, time_series: NDArrayFloat) -> str:
        x_min = np.min(time_series)
        x_max = np.max(time_series)

        self.boundaries = np.linspace(x_min, x_max, self.K + 1)
        self.centers = [(self.boundaries[i] + self.boundaries[i + 1]) / 2 for i in range(self.K)]

        indices = np.digitize(time_series, self.boundaries) - 1
        indices = np.clip(indices, 0, self.K - 1)

        return self.huffman.encode(indices.tolist())

    def decompress(self, bits: str) -> NDArrayFloat:
        decoded_indices = self.huffman.decode(bits)
        return np.array([self.centers[i] for i in decoded_indices], dtype=np.float64)

if __name__ == "__main__":
    ts = np.loadtxt("ts_homework_practicum_5.txt")

    compressor = LossyCompression()
    bits = compressor.compress(ts)
    decompressed_ts = compressor.decompress(bits)

    compression_ratio = (len(ts) * 32) / len(bits) 
    print(f"Compression ratio: {compression_ratio:.2f}")

    compression_loss = np.sqrt(np.mean((ts - decompressed_ts)**2))
    print(f"Compression loss (RMSE): {compression_loss}")

