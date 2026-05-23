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

        self.code_by_symbol = {}
        self.symbol_by_code = {}
        self.root = None
        self.single_symbol = None

    def encode(self, sequence: list[Any]) -> str:

        if len(sequence) == 0:
            self.code_by_symbol = {}
            self.symbol_by_code = {}
            self.root = None
            self.single_symbol = None
            return ""


        freq = {}
        for symbol in sequence:
            freq[symbol] = freq.get(symbol, 0) + 1


        if len(freq) == 1:
            symbol = next(iter(freq))
            self.single_symbol = symbol
            self.root = symbol
            self.code_by_symbol = {symbol: "0"}
            self.symbol_by_code = {"0": symbol}
            return "0" * len(sequence)

        self.single_symbol = None


        heap = []
        uid = 0
        for symbol, count in freq.items():
            heapq.heappush(heap, (count, uid, ("leaf", symbol)))
            uid += 1

        while len(heap) > 1:
            count1, _, left = heapq.heappop(heap)
            count2, _, right = heapq.heappop(heap)
            parent = ("node", left, right)
            heapq.heappush(heap, (count1 + count2, uid, parent))
            uid += 1

        self.root = heap[0][2]

        self.code_by_symbol = {}
        self.symbol_by_code = {}

        def build_codes(node, code):
            node_type = node[0]

            if node_type == "leaf":
                symbol = node[1]
                self.code_by_symbol[symbol] = code
                self.symbol_by_code[code] = symbol
                return

            _, left, right = node
            build_codes(left, code + "0")
            build_codes(right, code + "1")

        build_codes(self.root, "")

        encoded = ""
        for symbol in sequence:
            encoded += self.code_by_symbol[symbol]

        return encoded
        

    def decode(self, encoded_sequence: str) -> list[Any]:
        if encoded_sequence == "":
            return []


        if self.single_symbol is not None:
            return [self.single_symbol] * len(encoded_sequence)

        decoded = []
        current = self.root

        for bit in encoded_sequence:
            if bit == "0":
                current = current[1]
            else:
                current = current[2]

            if current[0] == "leaf":
                decoded.append(current[1])
                current = self.root

        return decoded
        


class LossyCompression:
    def __init__(self) -> None:
        self.num_levels = 256
        self.min_val = None
        self.max_val = None
        self.step = None
        self.huffman = HuffmanCoding()
        

    def compress(self, time_series: NDArrayFloat) -> str:

        if len(time_series) == 0:
            self.min_val = 0.0
            self.max_val = 0.0
            self.step = 0.0
            self.huffman = HuffmanCoding()
            return ""

        self.min_val = float(np.min(time_series))
        self.max_val = float(np.max(time_series))


        if self.max_val == self.min_val:
            quantized = [0] * len(time_series)
            self.step = 0.0
            self.huffman = HuffmanCoding()
            return self.huffman.encode(quantized)

        self.step = (self.max_val - self.min_val) / self.num_levels

        quantized = []
        for x in time_series:
            index = int((float(x) - self.min_val) / self.step)
            if index < 0:
                index = 0
            if index >= self.num_levels:
                index = self.num_levels - 1
            quantized.append(index)

        self.huffman = HuffmanCoding()
        bits = self.huffman.encode(quantized)
        return bits

    def decompress(self, bits: str) -> NDArrayFloat:

        if bits == "":
            return np.array([], dtype=float)

        quantized = self.huffman.decode(bits)


        if self.step == 0.0:
            return np.array([self.min_val] * len(quantized), dtype=float)

        decompressed = []
        for q in quantized:
            value = self.min_val + (q + 0.5) * self.step
            decompressed.append(value)

        return np.array(decompressed, dtype=float)


if __name__ == "__main__":
    ts = np.loadtxt("ts_homework_practicum_5.txt")

    compressor = LossyCompression()
    bits = compressor.compress(ts)
    decompressed_ts = compressor.decompress(bits)

    compression_ratio = (len(ts) * 32 * 8) / len(bits) 
    print(f"Compression ratio: {compression_ratio:.2f}")

    compression_loss = np.sqrt(np.mean((ts - decompressed_ts)**2))
    print(f"Compression loss (RMSE): {compression_loss}")

