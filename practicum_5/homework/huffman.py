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
        self.reverse_codes = {}

    def encode(self, sequence: list[Any]) -> str:
        if not sequence:
            return ""

        frequency = {}
        for symbol in sequence:
            frequency[symbol] = frequency.get(symbol, 0) + 1

        if len(frequency) == 1:
            symbol = next(iter(frequency.keys()))
            self.codes = {symbol: "0"}
            self.reverse_codes = {"0": symbol}
            return "0" * len(sequence)

        heap = [[freq,[symbol, ""]] for symbol, freq in frequency.items()]
        heapq.heapify(heap)

        while len(heap) > 1:
            x = heapq.heappop(heap)
            y = heapq.heappop(heap)
            for pair in x[1:]:
                pair[1] = "0" + pair[1]
            for pair in y[1:]:
                pair[1] = "1" + pair[1]
            heapq.heappush(heap, [x[0] + y[0]] + x[1:] + y[1:])

        leafs = heap[0][1:]
        self.codes = {symbol: code for symbol, code in leafs}
        self.reverse_codes = {code: symbol for symbol, code in leafs}

        return ''.join(self.codes[symbol] for symbol in sequence)

    def decode(self, encoded_sequence: str) -> list[Any]:
        result = []
        curr_code = ""

        for bit in encoded_sequence:
            curr_code += bit
            if curr_code in self.reverse_codes:
                result.append(self.reverse_codes[curr_code])
                curr_code = ""

        return result


class LossyCompression:
    def __init__(self, delta = 0.01, bits_per_sample = 8) -> None:
        self.huffman = HuffmanCoding()
        self.delta = delta
        self.bits_per_sample = bits_per_sample

    def compress(self, time_series: NDArrayFloat) -> str:
        levels = np.round(time_series / self.delta).astype(np.int64)

        max_level = 2**self.bits_per_sample - 1
        levels = np.clip(levels, 0, max_level)

        sequence = levels.tolist()

        bits = self.huffman.encode(sequence = sequence)

        return bits

    def decompress(self, bits: str) -> NDArrayFloat:
        symbols = self.huffman.decode(bits)

        levels = np.array(symbols)
        recovery = levels * self.delta

        return recovery


if __name__ == "__main__":
    ts = np.loadtxt("ts_homework_practicum_5.txt")

    compressor = LossyCompression()
    bits = compressor.compress(ts)
    decompressed_ts = compressor.decompress(bits)

    compression_ratio = (len(ts) * 32 * 8) / len(bits) 
    print(f"Compression ratio: {compression_ratio:.2f}")

    compression_loss = np.sqrt(np.mean((ts - decompressed_ts)**2))
    print(f"Compression loss (RMSE): {compression_loss}")

