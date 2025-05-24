from pathlib import Path
import heapq
from typing import Any, Optional
from abc import ABC, abstractmethod

import networkx as nx
import numpy as np

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph, NDArrayFloat


class HuffmanCoding:
    def __init__(self) -> None:
        self.codes = {}
        self.reverse_codes = {}

    def encode(self, sequence: list[Any]) -> str:
        freq = {}
        for item in sequence:
            freq[item] = freq.get(item, 0) + 1

        heap = [[weight, [symbol, ""]] for symbol, weight in freq.items()]
        heapq.heapify(heap) # преобразуем в кучу

        while len(heap) > 1:
            lo = heapq.heappop(heap) # берем первый узел
            hi = heapq.heappop(heap) # второй узел
            for pair in lo[1:]:
                pair[1] = "0" + pair[1]
            for pair in hi[1:]:
                pair[1] = "1" + pair[1]
            heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:]) # добавляем склеенный узел

        for pair in heap[0][1:]:
            self.codes[pair[0]] = pair[1]
            self.reverse_codes[pair[1]] = pair[0]

        return ''.join(self.codes[symbol] for symbol in sequence) # кортеж из 0 и 1

    def decode(self, encoded_sequence: str) -> list[Any]:
        result = []
        code = ""
        for bit in encoded_sequence:
            code += bit
            if code in self.reverse_codes:
                result.append(self.reverse_codes[code])
                code = ""
        return result


class LossyCompression:
    def __init__(self) -> None:
        self.num_gaps = 1000
        self.bin_edges = None
        self.middle_values = None
        self.huffman = HuffmanCoding()

    def compress(self, time_series: NDArrayFloat) -> str:
        min_val, max_val = np.min(time_series), np.max(time_series)
        self.bin_edges = np.linspace(min_val, max_val, self.num_gaps + 1)
        self.middle_values = (self.bin_edges[:-1] + self.bin_edges[1:]) * 0.5
        quantized = np.digitize(time_series, self.bin_edges) - 1 # индексы отрезков, в которых лежат точки
        quantized = np.clip(quantized, 0, self.num_gaps - 1) # корректность крайних случаев
        symbols = quantized.tolist()
        return self.huffman.encode(symbols)

    def decompress(self, bits: str) -> NDArrayFloat:
        symbols = self.huffman.decode(bits)
        return np.array([self.middle_values[s] for s in symbols])


if __name__ == "__main__":
    ts = np.loadtxt("ts_homework_practicum_5.txt")

    compressor = LossyCompression()
    bits = compressor.compress(ts)
    decompressed_ts = compressor.decompress(bits)

    compression_ratio = (len(ts) * 32 * 8) / len(bits)
    print(f"Compression ratio: {compression_ratio:.2f}")

    compression_loss = np.sqrt(np.mean((ts - decompressed_ts)**2))
    print(f"Compression loss (RMSE): {compression_loss}")
