import sys
from pathlib import Path

root_path = Path(__file__).resolve().parents[2]
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))

from pathlib import Path
import heapq
from typing import Any
from abc import ABC, abstractmethod
from collections import Counter

import networkx as nx
import numpy as np

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph, NDArrayFloat


class HuffmanCoding:
    def __init__(self) -> None:
        self.encoder = {}
        self.decoder = {}

    def encode(self, sequence: list[Any]) -> str:
        if not sequence:
            return ""
            
        counts = Counter(sequence)
        heap = []
        idx = 0
        
        for sym, freq in counts.items():
            heapq.heappush(heap, (freq, idx, sym, None, None))
            idx += 1
            
        while len(heap) > 1:
            f1, id1, s1, l1, r1 = heapq.heappop(heap)
            f2, id2, s2, l2, r2 = heapq.heappop(heap)
            parent = (f1 + f2, idx, None, (f1, id1, s1, l1, r1), (f2, id2, s2, l2, r2))
            idx += 1
            heapq.heappush(heap, parent)
            
        self.encoder = {}
        root = heap[0]
        stack = [(root, "")]
        
        while stack:
            node, code = stack.pop()
            freq, nid, sym, left, right = node
            if sym is not None:
                self.encoder[sym] = code
            else:
                if left is not None:
                    stack.append((left, code + "0"))
                if right is not None:
                    stack.append((right, code + "1"))
                    
        if len(counts) == 1:
            sym = list(counts.keys())[0]
            self.encoder[sym] = "0"
            
        self.decoder = {v: k for k, v in self.encoder.items()}
        
        result = []
        for sym in sequence:
            result.append(self.encoder[sym])
            
        return "".join(result)

    def decode(self, encoded_sequence: str) -> list[Any]:
        result = []
        current_code = ""
        for bit in encoded_sequence:
            current_code += bit
            if current_code in self.decoder:
                result.append(self.decoder[current_code])
                current_code = ""
        return result


class LossyCompression:
    def __init__(self) -> None:
        self.huffman = HuffmanCoding()
        self.min_val = 0.0
        self.step = 0.0
        self.centers = []

    def compress(self, time_series: NDArrayFloat) -> str:
        self.min_val = float(np.min(time_series))
        max_val = float(np.max(time_series))
        K = 64
        
        if max_val == self.min_val:
            self.step = 1.0
            self.centers = [self.min_val]
            indices = [0] * len(time_series)
        else:
            self.step = (max_val - self.min_val) / K
            self.centers = [self.min_val + (i + 0.5) * self.step for i in range(K)]
            indices = []
            for val in time_series:
                idx = int((val - self.min_val) / self.step)
                if idx >= K:
                    idx = K - 1
                if idx < 0:
                    idx = 0
                indices.append(idx)
                
        return self.huffman.encode(indices)

    def decompress(self, bits: str) -> NDArrayFloat:
        indices = self.huffman.decode(bits)
        reconstructed = []
        for idx in indices:
            reconstructed.append(self.centers[idx])
        return np.array(reconstructed, dtype=np.float64)


if __name__ == "__main__":
    ts = np.loadtxt("ts_homework_practicum_5.txt")

    compressor = LossyCompression()
    bits = compressor.compress(ts)
    decompressed_ts = compressor.decompress(bits)

    compression_ratio = (len(ts) * 32 * 8) / len(bits) 
    print(f"Compression ratio: {compression_ratio:.2f}")

    compression_loss = np.sqrt(np.mean((ts - decompressed_ts)**2))
    print(f"Compression loss (RMSE): {compression_loss}")