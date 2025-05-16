from pathlib import Path
import heapq
from typing import Any
from abc import ABC, abstractmethod

import networkx as nx
import numpy as np

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph, NDArrayFloat

class Node:
    def __init__(self, ch, freq, left=None, right=None):
        self.ch = ch
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

class HuffmanCoding:
    def __init__(self) -> None:
        self.root = None
        self.huffman_code = {}
        self.reverse_huffman_code = {}

    def encode(self, sequence: list[Any]) -> str:
        if not any(sequence):
            return ""
        
        freq = {}
        for item in sequence:
            freq[item] = freq.get(item, 0) + 1

        pq = [Node(k, v) for k, v in freq.items()]
        heapq.heapify(pq)

        while len(pq) > 1:
            left = heapq.heappop(pq)
            right = heapq.heappop(pq)
            total = left.freq + right.freq
            heapq.heappush(pq, Node(None, total, left, right))

        self.root = pq[0] if pq else None
        self.huffman_code = {}
        self.reverse_huffman_code = {}

        if self.root:
            stack = [(self.root, "")]
            while stack:
                node, code = stack.pop()
                if node.left is None and node.right is None:
                    self.huffman_code[node.ch] = code if code else '1'
                    self.reverse_huffman_code[code] = node.ch
                if node.right:
                    stack.append((node.right, code + '1'))
                if node.left:
                    stack.append((node.left, code + '0'))

        return ''.join([self.huffman_code[item] for item in sequence])

    def decode(self, encoded_sequence: str) -> list[Any]:
        if not any(encoded_sequence) or not self.root:
            return []

        if self.root.left is None and self.root.right is None:
            return [self.root.ch] * self.root.freq

        decoded = []
        current_node = self.root
        for bit in encoded_sequence:
            if bit == '0':
                current_node = current_node.left
            else:
                current_node = current_node.right

            if current_node.left is None and current_node.right is None:
                decoded.append(current_node.ch)
                current_node = self.root

        return decoded


class LossyCompression:
    def __init__(self) -> None:
        self.n = 8
        self.min_value = None
        self.max_value = None
        self.edges = None
        self.centers = None

    def compress(self, time_series: NDArrayFloat) -> str:
        self.min_value = np.min(time_series)
        self.max_value = np.max(time_series)
        self.edges = np.linspace(self.min_value, self.max_value, self.n + 1)
        self.centers = (self.edges[:-1] + self.edges[1:]) / 2

        indices = np.digitize(time_series, self.edges[1:-1], right=True)
        bits_per_symbol = int(np.ceil(np.log2(self.n)))
        bits = ''.join([format(idx, f'0{bits_per_symbol}b') for idx in indices])
        return bits
        
    def decompress(self, bits: str) -> NDArrayFloat:
        bits_per_symbol = int(np.ceil(np.log2(self.n)))
        indices = [int(bits[i:i+bits_per_symbol], 2) 
                  for i in range(0, len(bits), bits_per_symbol)]
        indices = np.clip(indices, 0, len(self.centers)-1)
        return np.array([self.centers[i] for i in indices])


if __name__ == "__main__":
    ts = np.loadtxt("ts_homework_practicum_5.txt")

    # compressor = LossyCompression()
    # bits = compressor.compress(ts)
    # decompressed_ts = compressor.decompress(bits)
    compressor = HuffmanCoding()
    bits = compressor.encode(ts)
    decompressed_ts = compressor.decode(bits)

    compression_ratio = (len(ts) * 32 * 8) / len(bits) 
    print(f"Compression ratio: {compression_ratio:.2f}")

    compression_loss = np.sqrt(np.mean((ts - decompressed_ts)**2))
    print(f"Compression loss (RMSE): {compression_loss}")

