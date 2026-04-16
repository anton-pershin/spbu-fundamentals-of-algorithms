from pathlib import Path
import heapq
from typing import Any
from collections import Counter

import numpy as np


class HuffmanCoding:
    def __init__(self) -> None:
        self.codes = {}
        self.reverse_codes = {}
        self.tree = None

    class Node:
        def __init__(self, symbol=None, freq=0):
            self.symbol = symbol
            self.freq = freq
            self.left = None
            self.right = None

        def __lt__(self, other):
            return self.freq < other.freq

    def _build_tree(self, sequence):
        freq = Counter(sequence)
        heap = [self.Node(sym, f) for sym, f in freq.items()]
        heapq.heapify(heap)

        while len(heap) > 1:
            n1 = heapq.heappop(heap)
            n2 = heapq.heappop(heap)

            merged = self.Node(freq=n1.freq + n2.freq)
            merged.left = n1
            merged.right = n2

            heapq.heappush(heap, merged)

        self.tree = heap[0]

    def _build_codes(self, node, current_code=""):
        if node is None:
            return

        if node.symbol is not None:
            self.codes[node.symbol] = current_code
            self.reverse_codes[current_code] = node.symbol
            return

        self._build_codes(node.left, current_code + "0")
        self._build_codes(node.right, current_code + "1")

    def encode(self, sequence: list[Any]) -> str:
        self._build_tree(sequence)
        self._build_codes(self.tree)

        encoded = "".join(self.codes[s] for s in sequence)
        return encoded

    def decode(self, encoded_sequence: str) -> list[Any]:
        decoded = []
        current_code = ""

        for bit in encoded_sequence:
            current_code += bit
            if current_code in self.reverse_codes:
                decoded.append(self.reverse_codes[current_code])
                current_code = ""

        return decoded


class LossyCompression:
    def __init__(self) -> None:
        self.num_levels = 16  
        self.min_val = None
        self.max_val = None
        self.huffman = HuffmanCoding()

    def _quantize(self, data):
        normalized = (data - self.min_val) / (self.max_val - self.min_val)

        indices = np.floor(normalized * (self.num_levels - 1)).astype(int)
        return indices

    def _dequantize(self, indices):
        normalized = indices / (self.num_levels - 1)
        values = normalized * (self.max_val - self.min_val) + self.min_val
        return values

    def compress(self, time_series: np.ndarray) -> str:
        self.min_val = np.min(time_series)
        self.max_val = np.max(time_series)

        quantized = self._quantize(time_series)
        quantized_list = quantized.tolist()

        bits = self.huffman.encode(quantized_list)
        return bits

    def decompress(self, bits: str) -> np.ndarray:
        decoded_indices = self.huffman.decode(bits)
        decoded_indices = np.array(decoded_indices)

        reconstructed = self._dequantize(decoded_indices)
        return reconstructed