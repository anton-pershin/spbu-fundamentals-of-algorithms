from pathlib import Path
import heapq
from typing import Any
from abc import ABC, abstractmethod

import networkx as nx
import numpy as np
import sys
sys.path.append(r"/Users/alexanderkuka/documents/python/pershin/spbu-fundamentals-of-algorithms")

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph, NDArrayFloat

class HuffmanCoding:
    def __init__(self) -> None:
        self.root = None
        self.codes: dict[Any, str] = {}

    def encode(self, sequence: list[Any]) -> str:
        freq = {}
        for symbol in sequence:
            freq[symbol] = freq.get(symbol, 0) + 1

        heap = []
        uid = 0  
        for symbol, count in freq.items():
            heapq.heappush(heap, (count, uid, (symbol, None, None)))
            uid += 1

        while len(heap) > 1:
            freq1, _, node1 = heapq.heappop(heap)
            freq2, _, node2 = heapq.heappop(heap)
        
            merged_node = (None, node1, node2)
            heapq.heappush(heap, (freq1 + freq2, uid, merged_node))
            uid += 1
        _, _, leaf = heap[0]
        self.root = (None, leaf, None)
       
        self.codes = {}
        def _generate_codes(node: tuple, code: str) -> None:
            symbol, left, right = node
            if symbol is not None:
                self.codes[symbol] = code if code else '0'
            else:
                if left: _generate_codes(left, code + '0')
                if right: _generate_codes(right, code + '1')
        
        _generate_codes(self.root, '')
        return ''.join(self.codes[s] for s in sequence)

    def decode(self, encoded_sequence: str) -> list[Any]:
        if self.root is None:
            return []

        decoded = []
        current_node = self.root
        for bit in encoded_sequence:
            symbol, left, right = current_node
            current_node = left if bit == '0' else right
            symbol, _, _ = current_node
            if symbol is not None:
                decoded.append(symbol)
                current_node = self.root
        return decoded


class LossyCompression:
    def __init__(self, levels: int = 16) -> None:
        self.levels = levels
        self.centers: np.ndarray | None = None 
        self.huffman = HuffmanCoding()

    def compress(self, time_series: NDArrayFloat) -> str:
        
        min_val, max_val = float(np.min(time_series)), float(np.max(time_series))
        bins = np.linspace(min_val, max_val, self.levels + 1)
        self.centers = (bins[:-1] + bins[1:]) / 2
        
        
        quantized = np.digitize(time_series, bins[1:-1], right=False)
        return self.huffman.encode(quantized.tolist())

    def decompress(self, bits: str) -> NDArrayFloat:
        symbols = self.huffman.decode(bits)
        return np.array([self.centers[s] for s in symbols], dtype=float)



if __name__ == "__main__":
    ts = np.loadtxt("pershin/spbu-fundamentals-of-algorithms/ts_homework_practicum_5.txt")

    compressor = LossyCompression()
    bits = compressor.compress(ts)
    decompressed_ts = compressor.decompress(bits)

    compression_ratio = (len(ts) * 32 * 8) / len(bits) 
    print(f"Compression ratio: {compression_ratio:.2f}")
    compression_loss = np.sqrt(np.mean((ts - decompressed_ts)**2))
    print(f"Compression loss (RMSE): {compression_loss}")

