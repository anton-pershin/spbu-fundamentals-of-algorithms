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
        self.codes = {}  
        self.tree = None  
        self.reverse_codes = {}  

    def encode(self, sequence: list[Any]) -> str:
        if not sequence:
            return ""
        
        frequencies = {}
        for symbol in sequence:
            frequencies[symbol] = frequencies.get(symbol, 0) + 1
        
        self._build_huffman_tree(frequencies)
        
        self._generate_codes(self.tree, "")
        
        encoded = ""
        for symbol in sequence:
            encoded += self.codes[symbol]
        
        return encoded
        

    def decode(self, encoded_sequence: str) -> list[Any]:
        if not encoded_sequence or not self.tree:
            return []
        
        decoded = []
        current_node = self.tree
        
        for bit in encoded_sequence:
            if isinstance(current_node, tuple) and len(current_node) == 2:
                if not isinstance(current_node[0], tuple) and not isinstance(current_node[1], tuple):
                    if bit == "0":
                        decoded.append(current_node[0])
                    else:
                        decoded.append(current_node[1])
                    current_node = self.tree
                    continue
            
            if bit == "0":
                if isinstance(current_node[0], tuple):
                    current_node = current_node[0]
                else:
                    decoded.append(current_node[0])
                    current_node = self.tree
            else:
                if isinstance(current_node[1], tuple):
                    current_node = current_node[1]
                else:
                    decoded.append(current_node[1])
                    current_node = self.tree
        
        return decoded
    
    def _build_huffman_tree(self, frequencies: dict) -> None:
        if not frequencies:
            return
        
        heap = []
        for symbol, freq in frequencies.items():
            heapq.heappush(heap, (freq, id(symbol), symbol))
        
        if len(heap) == 1:
            freq, _, symbol = heapq.heappop(heap)
            self.tree = (symbol, None)
            return
        
        counter = 0
        while len(heap) > 1:
            freq1, _, left = heapq.heappop(heap)
            freq2, _, right = heapq.heappop(heap)
            
            merged_freq = freq1 + freq2
            counter += 1
            heapq.heappush(heap, (merged_freq, counter, (left, right)))
        
        _, _, self.tree = heapq.heappop(heap)
    
    def _generate_codes(self, node, code: str) -> None:
        if node is None:
            return
        
        if not isinstance(node, tuple):
            self.codes[node] = code if code else "0"
            self.reverse_codes[code if code else "0"] = node
            return
        
        left, right = node
        
        if right is None:
            self.codes[left] = code if code else "0"
            self.reverse_codes[code if code else "0"] = left
            return
        
        self._generate_codes(left, code + "0")
        self._generate_codes(right, code + "1")


class LossyCompression:
    def __init__(self, num_levels: int = 256) -> None:
        self.num_levels = num_levels
        self.huffman = HuffmanCoding()
        self.data_min = None
        self.data_max = None
        self.interval_size = None

    def compress(self, time_series: NDArrayFloat) -> str:
        if len(time_series) == 0:
            return ""
        
        self.data_min = float(np.min(time_series))
        self.data_max = float(np.max(time_series))
        
        self.interval_size = (self.data_max - self.data_min) / self.num_levels
        if self.interval_size == 0:
            self.interval_size = 1.0
        
        quantized = self._quantize(time_series)
        
        encoded_data = self.huffman.encode(quantized.tolist())
        
        metadata = f"{self.data_min}|{self.data_max}|{self.num_levels}|"
        
        return metadata + encoded_data

    def decompress(self, bits: str) -> NDArrayFloat:
        if not bits or "|" not in bits:
            return np.array([])
        
        parts = bits.split("|", 3)
        if len(parts) < 4:
            return np.array([])
        
        self.data_min = float(parts[0])
        self.data_max = float(parts[1])
        self.num_levels = int(parts[2])
        encoded_data = parts[3]
        
        self.interval_size = (self.data_max - self.data_min) / self.num_levels
        if self.interval_size == 0:
            self.interval_size = 1.0
        
        quantized_indices = self.huffman.decode(encoded_data)
        
        decompressed = self._dequantize(np.array(quantized_indices))
        
        return decompressed
    
    def _quantize(self, time_series: NDArrayFloat) -> np.ndarray:
        if self.data_max == self.data_min:
            return np.zeros(len(time_series), dtype=int)
        
        normalized = (time_series - self.data_min) / (self.data_max - self.data_min)
        
        quantized = np.floor(normalized * (self.num_levels - 1)).astype(int)
        
        quantized = np.clip(quantized, 0, self.num_levels - 1)
        
        return quantized
    
    def _dequantize(self, quantized_indices: np.ndarray) -> NDArrayFloat:
        if self.data_max == self.data_min:
            return np.full(len(quantized_indices), self.data_min)
        
        normalized = quantized_indices / (self.num_levels - 1)
        
        decompressed = normalized * (self.data_max - self.data_min) + self.data_min
        
        return decompressed


if __name__ == "__main__":
    ts = np.loadtxt("ts_homework_practicum_5.txt")

    compressor = LossyCompression()
    bits = compressor.compress(ts)
    decompressed_ts = compressor.decompress(bits)

    compression_ratio = (len(ts) * 32 * 8) / len(bits) 
    print(f"Compression ratio: {compression_ratio:.2f}")

    compression_loss = np.sqrt(np.mean((ts - decompressed_ts)**2))
    print(f"Compression loss (RMSE): {compression_loss}")

