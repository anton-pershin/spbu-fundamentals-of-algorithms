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
        self.code_map = {}
        self.reverse_map = {}

    def encode(self, sequence: list[Any]) -> str:
        if not sequence:  # Проверка на пустую последовательность
            return ""
        frequencies = {}
        for item in sequence:
            frequencies[item] = frequencies.get(item, 0) + 1
        
        heap = [[weight, [symbol, ""]] for symbol, weight in frequencies.items()]
        heapq.heapify(heap)
       
        if not heap:
            return ""
       
        if len(heap) == 1:
            symbol_data = heapq.heappop(heap)
            self.code_map[symbol_data[1][0]] = "0"
        else:
            while len(heap) > 1:
                lo = heapq.heappop(heap)
                hi = heapq.heappop(heap)
                for pair in lo[1:]: pair[1] = '0' + pair[1]
                for pair in hi[1:]: pair[1] = '1' + pair[1]
                heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
           
            for pair in heapq.heappop(heap)[1:]:
                self.code_map[pair[0]] = pair[1]
       
        self.reverse_map = {v: k for k, v in self.code_map.items()}
        return "".join(self.code_map[item] for item in sequence) 

    def decode(self, encoded_sequence: str) -> list[Any]:

        decoded = []
        current_code = ""
        for bit in encoded_sequence:
            current_code += bit
            if current_code in self.reverse_map:
                decoded.append(self.reverse_map[current_code])
                current_code = ""
        return decoded


class LossyCompression:
    def __init__(self, K: int = 64) -> None:
        self.K = K
        self.huffman = HuffmanCoding()
        self.centers = None

    def compress(self, time_series: NDArrayFloat) -> str:

        min_val, max_val = np.min(time_series), np.max(time_series)
        bins = np.linspace(min_val, max_val, self.K + 1)
        self.centers = (bins[:-1] + bins[1:]) / 2
       
        indices = np.digitize(time_series, bins) - 1
        indices = np.clip(indices, 0, self.K - 1)
       
        return self.huffman.encode(list(indices))

    def decompress(self, bits: str) -> NDArrayFloat:

        indices = self.huffman.decode(bits)
        return np.array([self.centers[i] for i in indices])


if __name__ == "__main__":
    ts = np.loadtxt("ts_homework_practicum_5.txt")

    compressor = LossyCompression()
    bits = compressor.compress(ts)
    decompressed_ts = compressor.decompress(bits)

    compression_ratio = (len(ts) * 32 * 8) / len(bits) 
    print(f"Compression ratio: {compression_ratio:.2f}")

    compression_loss = np.sqrt(np.mean((ts - decompressed_ts)**2))
    print(f"Compression loss (RMSE): {compression_loss}")

