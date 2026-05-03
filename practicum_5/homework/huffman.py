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
        self.code_map = {}
        self.reverse_code_map = {}

    def encode(self, sequence: list[Any]) -> str:
        if not sequence:
            return ""

        frequencies = {}
        for item in sequence:
            frequencies[item] = frequencies.get(item, 0) + 1

        count = 0
        heap = []
        for symbol, freq in frequencies.items():
            heapq.heappush(heap, [freq, count, symbol])
            count += 1

        if len(heap) == 1:
            symbol = heap[0][2]
            self.code_map = {symbol: "0"}
            self.reverse_code_map = {"0": symbol}
            return "0" * len(sequence)

        while len(heap) > 1:
            lo = heapq.heappop(heap)
            hi = heapq.heappop(heap)

            combined = [lo[0] + hi[0], count, [lo[2], hi[2]]]
            count += 1
            heapq.heappush(heap, combined)

        tree = heap[0][2]

        self.code_map = {}

        def build_codes(node, current_code):
            if not isinstance(node, list):
                self.code_map[node] = current_code
                return
            build_codes(node[0], current_code + "0")
            build_codes(node[1], current_code + "1")

        build_codes(tree, "")

        self.reverse_code_map = {v: k for k, v in self.code_map.items()}

        return "".join(self.code_map[item] for item in sequence)
        

    def decode(self, encoded_sequence: str) -> list[Any]:
        res = []
        current_bits = ""

        for bit in encoded_sequence:
            current_bits += bit

            if current_bits in self.reverse_code_map:
                res.append(self.reverse_code_map[current_bits])
                current_bits = ""

        return res

class LossyCompression:
    def __init__(self) -> None:
        self.huffman = HuffmanCoding()
        self.k = 256

    def compress(self, time_series: NDArrayFloat) -> str:
        ts_min = np.min(time_series)
        ts_max = np.max(time_series)

        bins = np.linspace(ts_min, ts_max, self.k + 1)

        self.centers = (bins[:-1] + bins[1:]) / 2

        indices = np.digitize(time_series, bins) - 1
        indices = np.clip(indices, 0, self.k - 1)

        quantized_series = [float(self.centers[i]) for i in indices]

        return self.huffman.encode(quantized_series)

    def decompress(self, bits: str) -> NDArrayFloat:
        decompressed_list = self.huffman.decode(bits)

        return np.array(decompressed_list)


if __name__ == "__main__":
    ts = np.loadtxt("ts_homework_practicum_5.txt")

    compressor = LossyCompression()
    bits = compressor.compress(ts)
    decompressed_ts = compressor.decompress(bits)

    compression_ratio = (len(ts) * 32 * 8) / len(bits) 
    print(f"Compression ratio: {compression_ratio:.2f}")

    compression_loss = np.sqrt(np.mean((ts - decompressed_ts)**2))
    print(f"Compression loss (RMSE): {compression_loss}")