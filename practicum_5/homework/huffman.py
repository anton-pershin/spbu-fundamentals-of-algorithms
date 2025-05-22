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
        self.codebook = {}
        self.reverse_codebook = {}

    def encode(self, sequence: list[Any]) -> str:
        if not sequence:
            return ""

        frequency = {}
        for item in sequence:
            frequency[item] = frequency.get(item, 0) + 1

        heap = [[weight, [symbol, ""]] for symbol, weight in frequency.items()]
        heapq.heapify(heap)

        while len(heap) > 1:
            low = heapq.heappop(heap)
            high = heapq.heappop(heap)
            for pair in low[1:]:
                pair[1] = '0' + pair[1]
            for pair in high[1:]:
                pair[1] = '1' + pair[1]
            heapq.heappush(heap, [low[0] + high[0]] + low[1:] + high[1:])

        self.codebook = {symbol: code for symbol, code in heap[0][1:]}
        self.reverse_codebook = {code: symbol for symbol, code in self.codebook.items()}

        return ''.join([self.codebook[item] for item in sequence])

    def decode(self, encoded_sequence: str) -> list[Any]:
        cur_code = ""
        decoded = []
        for bit in encoded_sequence:
            cur_code += bit
            if cur_code in self.reverse_codebook:
                decoded.append(self.reverse_codebook[cur_code])
                cur_code = ""
        return decoded


class LossyCompression:
    def __init__(self) -> None:
        self.bins = None
        self.huffman = HuffmanCoding()

    def compress(self, time_series: NDArrayFloat) -> str:
        min_val, max_val = np.min(time_series), np.max(time_series)
        n_bins = 16
        bin_edges = np.linspace(min_val, max_val, n_bins + 1)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        quantized_idx = np.digitize(time_series, bin_edges[1:-1], right=True)
        self.bins = bin_centers
        return self.huffman.encode(quantized_idx.tolist())

    def decompress(self, bits: str) -> NDArrayFloat:
        decoded_idx = self.huffman.decode(bits)
        return np.array([self.bins[int(idx)] for idx in decoded_idx])


if __name__ == "__main__":
    ts = np.loadtxt("ts_homework_practicum_5.txt")

    compressor = LossyCompression()
    bits = compressor.compress(ts)
    decompressed_ts = compressor.decompress(bits)

    compression_ratio = (len(ts) * 32 * 8) / len(bits) 
    print(f"Compression ratio: {compression_ratio:.2f}")

    compression_loss = np.sqrt(np.mean((ts - decompressed_ts)**2))
    print(f"Compression loss (RMSE): {compression_loss}")

