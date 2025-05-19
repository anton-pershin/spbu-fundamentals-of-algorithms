from pathlib import Path
import heapq
from typing import Any, Dict, List, Tuple
from abc import ABC, abstractmethod

import networkx as nx
import numpy as np

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph, NDArrayFloat


class HuffmanCoding:
    def __init__(self) -> None:
        self.symbol_to_code: Dict[Any, str] = {}
        self.code_to_symbol: Dict[str, Any] = {}

    def _generate_codes(self, node: Any, prefix: str) -> None:
        if isinstance(node, list):
            self._generate_codes(node[0], prefix + '0')
            self._generate_codes(node[1], prefix + '1')
        else:
            self.symbol_to_code[node] = prefix
            self.code_to_symbol[prefix] = node

    def encode(self, sequence: List[Any]) -> str:
        freq: Dict[Any, int] = {}
        for item in sequence:
            freq[item] = freq.get(item, 0) + 1

        tree: List[Tuple[int, int, Any]] = []
        uid = 0
        for sym, f in freq.items():
            heapq.heappush(tree, (f, uid, sym))
            uid += 1

        while len(tree) > 1:
            f1, id1, left = heapq.heappop(tree)
            f2, id2, right = heapq.heappop(tree)
            merged = [left, right]
            heapq.heappush(tree, (f1 + f2, uid, merged))
            uid += 1
        
        self.symbol_to_code.clear()
        self.code_to_symbol.clear()
        self._generate_codes(tree[0][2], '')

        return ''.join(self.symbol_to_code[item] for item in sequence)

    def decode(self, encoded_sequence: str) -> List[Any]:
        decoded: List[Any] = []
        buffer = ''
        for bit in encoded_sequence:
            buffer += bit
            if buffer in self.code_to_symbol:
                decoded.append(self.code_to_symbol[buffer])
                buffer = ''
        return decoded


class LossyCompression:
    def __init__(self) -> None:
        self.min_val: float = 0.0
        self.max_val: float = 0.0
        self.levels: int = 256
        self.hf = HuffmanCoding()

    def compress(self, time_series: NDArrayFloat) -> str:
        self.min_val = float(np.min(time_series))
        self.max_val = float(np.max(time_series))
        if self.max_val == self.min_val:
            q = np.zeros_like(time_series, dtype=int)
        else:
            delta = (self.max_val - self.min_val) / self.levels
            normalized = (time_series - self.min_val) / delta
            q = np.floor(normalized).astype(int)
            q = np.clip(q, 0, self.levels - 1)

        return self.hf.encode(q)

    def decompress(self, bits: str) -> NDArrayFloat:
        q = np.array(self.hf.decode(bits))

        delta = (self.max_val - self.min_val) / self.levels
        return self.min_val + q * delta


if __name__ == "__main__":
    ts = np.loadtxt("ts_homework_practicum_5.txt")

    compressor = LossyCompression()
    bits = compressor.compress(ts)
    decompressed_ts = compressor.decompress(bits)

    compression_ratio = (len(ts) * 32 * 8) / len(bits) 
    print(f"Compression ratio: {compression_ratio:.2f}")

    compression_loss = np.sqrt(np.mean((ts - decompressed_ts)**2))
    print(f"Compression loss (RMSE): {compression_loss}")

