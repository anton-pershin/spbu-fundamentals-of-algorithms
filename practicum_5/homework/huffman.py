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
        self.root = None
        self.codes: dict[Any, str] = {}

    def encode(self, sequence: list[Any]) -> str:
        freq: dict[Any, int] = {}
        for sym in sequence:
            freq[sym] = freq.get(sym, 0) + 1
        heap: list[tuple[int, int, tuple[Any, Any, Any]]] = []
        counter = 0
        for sym, f in freq.items():
            heapq.heappush(heap, (f, counter, (sym, None, None)))
            counter += 1
        if len(heap) == 1:
            _, _, leaf = heap[0]
            self.root = (None, leaf, None)
        else:
            while len(heap) > 1:
                f1, c1, n1 = heapq.heappop(heap)
                f2, c2, n2 = heapq.heappop(heap)
                merged = (None, n1, n2)
                heapq.heappush(heap, (f1 + f2, counter, merged))
                counter += 1
            _, _, self.root = heap[0]
        self.codes = {}
        def traverse(node: tuple[Any, Any, Any], prefix: str) -> None:
            symbol, left, right = node
            if symbol is not None:
                self.codes[symbol] = prefix or '0'
            else:
                if left is not None:
                    traverse(left, prefix + '0')
                if right is not None:
                    traverse(right, prefix + '1')
        traverse(self.root, '')
        return ''.join(self.codes[s] for s in sequence)
        

    def decode(self, encoded_sequence: str) -> list[Any]:
        if self.root is None:
            return []
        result: list[Any] = []
        node = self.root
        for bit in encoded_sequence:
            symbol, left, right = node
            node = left if bit == '0' else right
            sym, _, _ = node
            if sym is not None:
                result.append(sym)
                node = self.root
        return result


class LossyCompression:
    def __init__(self) -> None:
        self.levels = 16
        self.centers: np.ndarray | None = None
        self.huffman = HuffmanCoding()

    def compress(self, time_series: NDArrayFloat) -> str:
        t_min, t_max = float(np.min(time_series)), float(np.max(time_series))
        edges = np.linspace(t_min, t_max, self.levels + 1)
        self.centers = (edges[:-1] + edges[1:]) / 2
        idx = np.digitize(time_series, edges[1:-1], right=False)
        idx = idx.astype(int)
        symbols = idx.tolist()
        bits = self.huffman.encode(symbols)
        return bits

    def decompress(self, bits: str) -> NDArrayFloat:
        if self.centers is None:
            raise ValueError("Compress firslty to set centers of quantization.")
        symbols = self.huffman.decode(bits)
        return np.array([self.centers[s] for s in symbols], dtype=float)


if __name__ == "__main__":
    ts = np.loadtxt("ts_homework_practicum_5.txt")

    compressor = LossyCompression()
    bits = compressor.compress(ts)
    decompressed_ts = compressor.decompress(bits)

    compression_ratio = (len(ts) * 32 * 8) / len(bits) 
    print(f"Compression ratio: {compression_ratio:.2f}")

    compression_loss = np.sqrt(np.mean((ts - decompressed_ts)**2))
    print(f"Compression loss (RMSE): {compression_loss}")

