from pathlib import Path
import heapq
from typing import Any
from abc import ABC, abstractmethod

import networkx as nx
import numpy as np

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph, NDArrayFloat

class Node:
    __slots__ = ('freq', 'symbol', 'left', 'right')
    
    def __init__(self, freq, symbol=None, left=None, right=None):
        self.freq = freq
        self.symbol = symbol
        self.left = left
        self.right = right
    
    def __lt__(self, other):
        return self.freq < other.freq
    
    def is_leaf(self) -> bool:
        return self.symbol is not None


class HuffmanNode:
    def __init__(self):
        self.root = None
        self.codes = {}
    
    def encode(self, sequence: list[Any]) -> str:
        if not sequence:
            return ""

        freq = {}
        for sym in sequence:
            freq[sym] = freq.get(sym, 0) + 1

        if len(freq) == 1:
            symbol = next(iter(freq.keys()))
            self.codes = {symbol: "0"}
            self.root = Node(freq=None, symbol=symbol)
            return "0" * len(sequence)

        heap = [Node(f, sym) for sym, f in freq.items()]
        heapq.heapify(heap)

        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            parent = Node(left.freq + right.freq, left=left, right=right)
            heapq.heappush(heap, parent)

        self.root = heap[0]
        self._build_codes(self.root, "")

        return ''.join(self.codes[sym] for sym in sequence)
    
    def _build_codes(self, node: Node, code: str) -> None:
        if node.is_leaf():
            self.codes[node.symbol] = code
        else:
            self._build_codes(node.left, code + '0')
            self._build_codes(node.right, code + '1')
    
    def decode(self, encoded_sequence: str) -> list[Any]:
        if not encoded_sequence or self.root is None:
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
    def __init__(self, delta=0.01, bits_per_sample=8) -> None:
        self.huffman = HuffmanNode()
        self.delta = delta
        self.bits_per_sample = bits_per_sample

    def compress(self, time_series: NDArrayFloat) -> str:
        levels = np.round(time_series / self.delta).astype(np.int64)
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