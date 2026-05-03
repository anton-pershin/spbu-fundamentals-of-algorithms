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
        freq = {}
        for s in sequence:
            freq[s] = freq.get(s, 0) + 1

        counter = 0
        heap = []
        for symbol, f in freq.items():
            node = {
                "symbol": symbol,
                "left": None,
                "right": None
            }
            heapq.heappush(heap, (f, counter, node))
            counter += 1

        while len(heap) > 1:
            f1, _, left_node = heapq.heappop(heap)
            f2, _, right_node = heapq.heappop(heap)
            new_node = {
                "symbol": None,
                "left": left_node,
                "right": right_node
            }
            heapq.heappush(heap, (f1 + f2, counter, new_node))
            counter += 1

        self.root = heap[0][2]
        self.codes = {}

        def build_codes(node, code=""):
            if node["symbol"] is not None:
                self.codes[node["symbol"]] = code if code != "" else "0"
                return

            build_codes(node["left"], code + "0")
            build_codes(node["right"], code + "1")

        build_codes(self.root)
        self.reverse_codes = {v: k for k, v in self.codes.items()}

        return "".join(self.codes[s] for s in sequence)
        

    def decode(self, encoded_sequence: str) -> list[Any]:
        result = []
        node = self.root

        for bit in encoded_sequence:
            if bit == "0":
                node = node["left"]
            else:
                node = node["right"]

            if node["symbol"] is not None:
                result.append(node["symbol"])
                node = self.root

        return result


class LossyCompression:
    def __init__(self) -> None:
        self.huffman = None
        self.K = 16
        self.centers = None
        self.z = None

    def compress(self, time_series: NDArrayFloat) -> str:
        self.huffman = HuffmanCoding()
        x_min = np.min(time_series)
        x_max = np.max(time_series)

        self.z = np.linspace(x_min, x_max, self.K + 1)

        self.centers = []
        for i in range(self.K):
            center = (self.z[i] + self.z[i + 1]) / 2
            self.centers.append(center)

        indices = np.digitize(time_series, self.z) - 1
        indices = np.clip(indices, 0, self.K - 1)
        quantized_indices = indices.tolist()

        bits = self.huffman.encode(quantized_indices)
        return bits

    def decompress(self, bits: str) -> NDArrayFloat:
        decoded_indices = self.huffman.decode(bits)  
        return np.array([self.centers[i] for i in decoded_indices])


if __name__ == "__main__":
    ts = np.loadtxt("ts_homework_practicum_5.txt")

    compressor = LossyCompression()
    bits = compressor.compress(ts)
    decompressed_ts = compressor.decompress(bits)

    compression_ratio = (len(ts) * 32 * 8) / len(bits) 
    print(f"Compression ratio: {compression_ratio:.2f}")

    compression_loss = np.sqrt(np.mean((ts - decompressed_ts)**2))
    print(f"Compression loss (RMSE): {compression_loss}")

