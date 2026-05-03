from pathlib import Path
import heapq
from typing import Any
from abc import ABC, abstractmethod

import networkx as nx
import numpy as np

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph, NDArrayFloat

class Node:
    def __init__(self, freq, symbol=None, left=None, right=None):
        self.freq = freq
        self.symbol = symbol
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq


class HuffmanCoding:
    def __init__(self) -> None:
        self.root = None
        self.code = {}
        self.dec = {}

    def encode(self, sequence: list[Any]) -> str:

        frequency = {}
        for s in sequence:
            frequency[s] = frequency.get(s, 0) + 1 

        heap = []
        for symbol, freq_i in frequency.items():
            heapq.heappush(heap, Node(freq_i, symbol))
        while len(heap) > 1:
            n_l = heapq.heappop(heap)
            n_r = heapq.heappop(heap)
            parent = Node(n_l.freq + n_r.freq, None, n_l, n_r)
            heapq.heappush(heap, parent)

        self.root = heap[0]

        def build(node, code_str=""):
            if node is None:
                return

            if node.symbol is not None:
                self.code[node.symbol] = code_str
                self.dec[code_str] = node.symbol
                return
            build(node.left, code_str + "0")
            build(node.right, code_str + "1")

        build(self.root)

        return "".join(self.code[s] for s in sequence)
        

    def decode(self, encoded_sequence: str) -> list[Any]:
        result = []
        current = ""
        for bit in encoded_sequence:
            current += bit
            if current in self.dec:
                result.append(self.dec[current])
                current = ""


class LossyCompression:
    def __init__(self) -> None:
        self.k = 32
        self.z_min = None
        self.z_max = None
        self.step = 0
        self.huffman = HuffmanCoding()

    def compress(self, time_series: NDArrayFloat) -> str:
        self.z_min = np.min(time_series)
        self.z_max = np.max(time_series)
        self.step = (self.z_max - self.z_min) / self.k

        quantized = []
        for x in time_series:
            i = int((x - self.z_min) / self.step)
            if i == self.k:
                i -= 1
            quantized.append(i)

        coded = self.huffman.encode(quantized)
        return coded

    def decompress(self, bits: str) -> NDArrayFloat:

        indices = self.huffman.decode(bits)
        decompressed = []
        for i in indices:
            z_i = self.z_min + i * self.step
            z_next = z_i + self.step
            x_i = (z_i + z_next) / 2
            decompressed.append(x_i)
        return np.array(decompressed)


if __name__ == "__main__":
    ts = np.loadtxt("ts_homework_practicum_5.txt")

    compressor = LossyCompression()
    bits = compressor.compress(ts)
    decompressed_ts = compressor.decompress(bits)

    compression_ratio = (len(ts) * 32 * 8) / len(bits) 
    print(f"Compression ratio: {compression_ratio:.2f}")

    compression_loss = np.sqrt(np.mean((ts - decompressed_ts)**2))
    print(f"Compression loss (RMSE): {compression_loss}")

