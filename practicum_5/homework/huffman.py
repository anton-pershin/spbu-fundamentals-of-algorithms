from pathlib import Path
import heapq
from typing import Any
# from abc import ABC, abstractmethod

# import networkx as nx
import numpy as np

# from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph, NDArrayFloat


class HuffmanCoding:
    def __init__(self) -> None:
        self.codes = {}
        self.rev = {}  # reverse

    def encode(self, sequence: list[Any]) -> str:
        freq = {}  # frequency
        for el in sequence:
            freq[el] = freq.get(el, 0) + 1
        heap = [[f, [s, '']] for s, f in freq.items()]  # heap, frequency, symbol
        heapq.heapify(heap)

        while len(heap) > 1:
            node_1 = heapq.heappop(heap)
            node_2 = heapq.heappop(heap)
            for el in node_1[1:]:
                el[1] = '0' + el[1]
            for el in node_2[1:]:
                el[1] = '1' + el[1]

            n_node = [node_1[0] + node_2[0]] + node_1[1:] + node_2[1:]
            heapq.heappush(heap, n_node)

        for el in heap[0][1:]:
            self.codes[el[0]] = el[1]
            self.rev[el[1]] = el[0]

        res = ''.join(self.codes[s] for s in sequence)  # result

        return res

    def decode(self, encoded_sequence: str) -> list[Any]:
        res = []
        cur = ''  # current

        for bit in encoded_sequence:
            cur += bit
            if cur in self.rev:
                res.append(self.rev[cur])
                cur = ''

        return res


class LossyCompression:
    def __init__(self) -> None:
        self.k = 64
        self.z_min = None
        self.z_max = None
        self.step = None
        self.huffman_coding = HuffmanCoding()

    def compress(self, time_series: NDArrayFloat) -> str:
        self.z_min = float(np.min(time_series))
        self.z_max = float(np.max(time_series))
        self.step = (self.z_max - self.z_min) / self.k

        quan = []  # quantized
        for x in time_series:
            i = int((x - self.z_min) / self.step)  # index
            if i >= self.k:
                i -= 1
            quan.append(i)

        res = self.huffman_coding.encode(quan)
        return res

    def decompress(self, bits: str) -> NDArrayFloat:
        ids = self.huffman_coding.decode(bits)  # indices
        res = []

        for i in ids:
            l = self.z_min + i * self.step  # left
            r = l + self.step  # right
            mid = (l + r) / 2
            res.append(mid)

        return np.array(res)


if __name__ == "__main__":
    ts = np.loadtxt("ts_homework_practicum_5.txt")

    compressor = LossyCompression()
    bits = compressor.compress(ts)
    decompressed_ts = compressor.decompress(bits)

    compression_ratio = (len(ts) * 32 * 8) / len(bits)
    print(f"Compression ratio: {compression_ratio:.2f}")

    compression_loss = np.sqrt(np.mean((ts - decompressed_ts) ** 2))
    print(f"Compression loss (RMSE): {compression_loss}")

