from pathlib import Path
import heapq as hq
from typing import Any
from abc import ABC, abstractmethod
from collections import Counter

import networkx as nx
import numpy as np

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph, NDArrayFloat


class HuffmanCoding:
    def __init__(self) -> None:
        self.codes: dict[any, str] = {}
        self.reverse_codes: dict [str, any] = {}
        self.is_built = False

    def _build_tree_and_codes(self, sequence: list[Any]) -> None:
        frequencies = Counter(sequence)
        heap = []

        for i, (symbol, freq) in enumerate(frequencies.items()):
            hq.heappush(heap, (freq, i, None, None, symbol))

        next_index = len(frequencies)

        while len(heap) > 1:
            freq1, idx1, left1, right1, symbol1 = hq.heappop(heap)
            freq2, idx2, left2, right2, symbol2 = hq.heappop(heap)

            new_freq = freq1 + freq2

            new_node = (new_freq, next_index, (freq1, idx1, left1, right1, symbol1), 
                       (freq2, idx2, left2, right2, symbol2), None)
            hq.heappush(heap, new_node)
            next_index += 1
        root = heap[0]
        
        def dfs(node, current_code):
            freq, idx, left, right, symbol = node
            
            if symbol is not None:
                self.codes[symbol] = current_code
                self.reverse_codes[current_code] = symbol
                return
            
            if left is not None:
                dfs(left, current_code + '0')
            if right is not None:
                dfs(right, current_code + '1')
        
        dfs(root, '')
        self.is_built = True

    def encode(self, sequence: list[Any]) -> str:

        if not self.is_built:
            self._build_tree_and_codes(sequence)
        
        encoded_parts = []
        for symbol in sequence:
            if symbol not in self.codes:
                raise ValueError(f" {symbol} not found")
            encoded_parts.append(self.codes[symbol])
        
        return ''.join(encoded_parts)

    def decode(self, encoded_sequence: str) -> list[Any]:
        if not self.is_built:
            raise RuntimeError("Need encode")
        
        result = []
        current_code = ""
        
        for bit in encoded_sequence:
            current_code += bit

            if current_code in self.reverse_codes:
                result.append(self.reverse_codes[current_code])
                current_code = ""

        if current_code:
            raise ValueError(f"failed decode: {current_code}")
        
        return result

class LossyCompression:
    def __init__(self, K: int = 16):
        self.K = K
        self.min_val = None
        self.max_val = None
        self.centers = None
        self.huffman = HuffmanCoding()


    def _quantize(self, time_series: NDArrayFloat) -> list[float]:
            
            self.min_val = float(np.min(time_series))
            self.max_val = float(np.max(time_series))
            
            if self.min_val == self.max_val:
                self.centers = [self.min_val]
                return [self.min_val] * len(time_series)
            
            interval_width = (self.max_val - self.min_val) / self.K
            
            self.centers = []
            for i in range(self.K):
                left = self.min_val + i * interval_width
                right = self.min_val + (i + 1) * interval_width
                center = (left + right) / 2
                self.centers.append(center)
            
            quantized = []
            for x in time_series:
                if x >= self.max_val:
                    idx = self.K - 1
                else:
                    idx = int((x - self.min_val) / interval_width)
                    idx = min(idx, self.K - 1)
                quantized.append(self.centers[idx])
            
            return quantized
    
    def compress(self, time_series: NDArrayFloat) -> str:

        quantized_sequence = self._quantize(time_series)
        bits = self.huffman.encode(quantized_sequence)
        
        return bits

    def decompress(self, bits: str) -> NDArrayFloat:

        quantized_sequence = self.huffman.decode(bits)

        return np.array(quantized_sequence, dtype=np.float64)

if __name__ == "__main__":
    ts = np.loadtxt("ts_homework_practicum_5.txt")

    compressor = LossyCompression()
    bits = compressor.compress(ts)
    decompressed_ts = compressor.decompress(bits)

    compression_ratio = (len(ts) * 32 * 8) / len(bits) 
    print(f"Compression ratio: {compression_ratio:.2f}")

    compression_loss = np.sqrt(np.mean((ts - decompressed_ts)**2))
    print(f"Compression loss (RMSE): {compression_loss}")