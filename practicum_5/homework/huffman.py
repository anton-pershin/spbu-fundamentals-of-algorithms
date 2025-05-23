from pathlib import Path
import heapq
from typing import Any
from abc import ABC, abstractmethod
import networkx as nx
import numpy as np
from collections import defaultdict

import sys
sys.path.append(r"/home/viktoria/algoritms/spbu-fundamentals-of-algorithms")

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph, NDArrayFloat


class HuffmanCoding:
    def __init__(self) -> None:
        self.codes = {}
        self.reverse_codes = {}

    def encode(self, sequence: list[Any]) -> str:
        freq = defaultdict(int)
        for symbol in sequence:
            freq[symbol] += 1

        heap = [[weight, [symbol, ""]] for symbol, weight in freq.items()]
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
        self.codes = {symbol: code for symbol, code in huff_pairs}
        self.reverse_codes = {code: symbol for symbol, code in huff_pairs}

        return ''.join(self.codes[symbol] for symbol in sequence)

    def decode(self, encoded_sequence: str) -> list[Any]:
        result = []
        current_code = ""
        
        for bit in encoded_sequence:
            current_code += bit
            if current_code in self.reverse_codes:
                result.append(self.reverse_codes[current_code])
                current_code = ""
        
        return result


class LossyCompression:
    def __init__(self, K: int = 256) -> None:
        self.K = K
        self.huffman = HuffmanCoding()
        self.min_val = None
        self.max_val = None
        self.bins = None
        self.centers = None

    def compress(self, time_series: NDArrayFloat) -> str:
        self.min_val = np.min(time_series)
        self.max_val = np.max(time_series)
        
        self.bins = np.linspace(self.min_val, self.max_val, self.K + 1)
        self.centers = (self.bins[:-1] + self.bins[1:]) / 2
        
        inds = np.digitize(time_series, self.bins) - 1
        inds[inds == self.K] = self.K - 1
        
        return self.huffman.encode(inds.tolist())

    def decompress(self, bits: str) -> NDArrayFloat:
        inds = self.huffman.decode(bits)
        return np.array([self.centers[i] for i in inds])


if __name__ == "__main__":
    ts = np.loadtxt("practicum_5/homework/ts_homework_practicum_5.txt")

    compressor = LossyCompression()
    bits = compressor.compress(ts)
    decompressed_ts = compressor.decompress(bits)

    original_bits = len(ts) * 32
    compressed_bits = len(bits)
    compression_ratio = original_bits / compressed_bits
    
    rmse = np.sqrt(np.mean((ts - decompressed_ts)**2))

    print(f"Compression ratio: {compression_ratio:.2f}")
    print(f"Compression loss (RMSE): {rmse:.6f}")
