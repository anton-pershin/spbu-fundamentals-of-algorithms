from pathlib import Path
import heapq
from typing import *
from abc import ABC, abstractmethod

import networkx as nx
import numpy as np

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph, NDArrayFloat

class HuffmanNode:
    def __init__(self, freq: int, symbol: Any = None, left: 'HuffmanNode' = None, right: 'HuffmanNode' = None):
        self.freq = freq
        self.symbol = symbol
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

class HuffmanCoding:
    
    def __init__(self) -> None:
        self.codes: Dict[Any, str] = {}
        self.reverse_codes: Dict[str, Any] = {}
        self.tree: HuffmanNode = None

    def build_tree(self, frequency: Dict[Any, int]) -> HuffmanNode:
        heap = [HuffmanNode(freq, symbol) for symbol, freq in frequency.items()]
        heapq.heapify(heap)
        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            merged = HuffmanNode(left.freq + right.freq, left=left, right=right)
            heapq.heappush(heap, merged)
        return heap[0]

    def build_codes_helper(self, node: HuffmanNode, current_code: str) -> None:
        if node is None:
            return
        if node.symbol is not None:
            self.codes[node.symbol] = current_code
            self.reverse_codes[current_code] = node.symbol
            return
        self.build_codes_helper(node.left, current_code + "0")
        self.build_codes_helper(node.right, current_code + "1")

    def encode(self, sequence: List[Any]) -> str:
        frequency = {}
        for symbol in sequence:
            frequency[symbol] = frequency.get(symbol, 0) + 1
        self.tree = self.build_tree(frequency)
        self.codes = {}
        self.reverse_codes = {}
        self.build_codes_helper(self.tree, "")
        encoded_str = "".join(self.codes[symbol] for symbol in sequence)
        return encoded_str

    def decode(self, encoded_sequence: str) -> List[Any]:
        decoded = []
        current_code = ""
        for bit in encoded_sequence:
            current_code += bit
            if current_code in self.reverse_codes:
                decoded.append(self.reverse_codes[current_code])
                current_code = ""
        return decoded

class LossyCompression:
    def __init__(self, num_levels: int = 16) -> None:
        self.num_levels = num_levels
        self.quantization_levels = None
        self.huffman = HuffmanCoding()

    def compress(self, time_series: np.ndarray) -> str:
        min_val, max_val = time_series.min(), time_series.max()
        self.quantization_levels = np.linspace(min_val, max_val, self.num_levels)
        indices = np.searchsorted(self.quantization_levels, time_series, side='right') - 1
        indices = np.clip(indices, 0, self.num_levels - 1)
        encoded_bits = self.huffman.encode(indices.tolist())
        return encoded_bits

    def decompress(self, bits: str) -> np.ndarray:
        indices = self.huffman.decode(bits)
        indices = np.array(indices)
        decompressed = self.quantization_levels[indices]
        return decompressed


if __name__ == "__main__":

    ts = np.loadtxt("practicum_5/homework/ts_homework_practicum_5.txt", encoding='utf-8')

    compressor = LossyCompression()
    bits = compressor.compress(ts)
    decompressed_ts = compressor.decompress(bits)

    compression_ratio = (len(ts) * 32 * 8) / len(bits) 
    print(f"Compression ratio: {compression_ratio:.2f}")

    compression_loss = np.sqrt(np.mean((ts - decompressed_ts)**2))
    print(f"Compression loss (RMSE): {compression_loss}")

