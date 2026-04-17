from pathlib import Path
import heapq
from typing import Any
from abc import ABC, abstractmethod

import networkx as nx
import numpy as np

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph, NDArrayFloat

class Node:
    def __init__(self, frequency, symbol = None, left = None, right = None) -> None:
        self.frequency = frequency
        self.symbol = symbol
        self.right = right
        self.left = left

    def __lt__(self, other):
        return self.frequency < other.frequency

    def is_leaf(self) -> bool:
        return self.symbol is not None

class HuffmanCoding:
    def __init__(self) -> None:
        self.codes = {}
        self.root = None

    def encode(self, sequence: list[Any]) -> str:
        if not sequence:
            return ""
        
        frequency = {}
        for symbol in sequence:
            frequency[symbol] = frequency.get(symbol, 0) + 1

        if len(frequency) == 1:
            symbol = next(iter(frequency.keys()))
            self.codes = {symbol: "0"}
            self.root = Node(frequency = None, symbol = symbol)
            return "0" * len(sequence)
        
        heap = [Node(frequency = freq, symbol = symbol) for symbol, freq in frequency.items()]
        heapq.heapify(heap)

        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            parent = Node(frequency = left.frequency + right.frequency, left = left, right = right)
            heapq.heappush(heap, parent)

        self.root = heap[0]
        self._build_codes(self.root, "")
        self.root = self._build_tree_from_codes(self.codes)

        return ''.join(self.codes[symbol] for symbol in sequence)

    def _build_codes(self, node: Node, code: str) -> None:
        if node.is_leaf():
            self.codes[node.symbol] = code
        else:
            self._build_codes(node.left, code + '0')
            self._build_codes(node.right, code + '1')

    def _build_tree_from_codes(self, codes):
        root = Node(frequency=None)
        for sym, code in codes.items():
            node = root
            for bit in code:
                if bit == '0':
                    if node.left is None:
                        node.left = Node(frequency=None)
                    node = node.left
                else:
                    if node.right is None:
                        node.right = Node(frequency=None)
                    node = node.right
            node.symbol = sym
        return root
    
    def decode(self, encoded_sequence: str) -> list[Any]:
        if not encoded_sequence:
            return []

        if self.root.is_leaf():
            return [self.root.symbol] * len(encoded_sequence)
        
        result = []
        node = self.root
        for bit in encoded_sequence:
            node = node.left if bit == '0' else node.right
            if node.is_leaf():
                result.append(node.symbol)
                node = self.root
        
        return result


class LossyCompression:
    def __init__(self, delta = 0.01, bits_per_sample = 8) -> None:
        self.huffman = HuffmanCoding()
        self.bits_per_sample = bits_per_sample
        self.delta = delta

    def compress(self, time_series: NDArrayFloat) -> str:
        data_range = time_series.max() - time_series.min()
        optimal_delta = data_range / (2**self.bits_per_sample - 1)
        self.delta = optimal_delta
    
        levels = np.round(time_series / optimal_delta).astype(np.int64)

        max_level = 2**self.bits_per_sample - 1
        levels = np.clip(levels, 0, max_level)

        return self.huffman.encode(levels.tolist())

    def decompress(self, bits: str) -> NDArrayFloat:
        symbols = self.huffman.decode(bits)
        return np.array(symbols) * self.delta


if __name__ == "__main__":
    ts = np.loadtxt("ts_homework_practicum_5.txt")

    compressor = LossyCompression()
    bits = compressor.compress(ts)
    decompressed_ts = compressor.decompress(bits)

    compression_ratio = (len(ts) * 32 * 8) / len(bits) 
    print(f"Compression ratio: {compression_ratio:.2f}")

    compression_loss = np.sqrt(np.mean((ts - decompressed_ts)**2))
    print(f"Compression loss (RMSE): {compression_loss}")

