from pathlib import Path
import heapq
from typing import Any
from abc import ABC, abstractmethod

import networkx as nx
import numpy as np

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph, NDArrayFloat

class Node:
    def __init__(self, char=None, frequency=None):
        self.char = char
        self.frequency = frequency
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.frequency < other.frequency


class HuffmanCoding:
    def __init__(self) -> None:
        self.codes = {}
        self.decode_map = {}
        self.b  = None

    def encode(self, sequence: list[Any]) -> str:
        freq = {}
        for c in sequence:
            if c in freq:
                freq[c]+=1
            else:
                freq[c] = 1
        priority_queue = [Node(char, f) for char, f in freq.items()]
        heapq.heapify(priority_queue)

        while len(priority_queue) > 1:
            left = heapq.heappop(priority_queue)
            right = heapq.heappop(priority_queue)

            merged = Node(frequency=left.frequency + right.frequency)
            merged.left = left
            merged.right = right

            heapq.heappush(priority_queue, merged)

        root = priority_queue[0]
        def build(node, code=""):
            if node.char is not None:
                self.codes[node.char] = code
                self.decode_map[code] = node.char
                return

            build(node.left, code + "0")
            build(node.right, code + "1")
        build(root)
        return "".join(self.codes[s] for s in sequence)
                        

    def decode(self, encoded_sequence: str) -> list[Any]:
        decoded = []
        cur_code = ""
        for bit in encoded_sequence:
            cur_code+=bit
            if cur_code in self.decode_map:
                decoded.append(self.decode_map[cur_code])
                cur_code = ""
        return decoded



class LossyCompression:
    def __init__(self) -> None:
        self.K = 32
        self.b = None
        self.centres = None
        self.huffman = HuffmanCoding()

    def compress(self, time_series: NDArrayFloat) -> str:
        xmin = np.min(time_series)
        xmax = np.max(time_series)
        gran = np.linspace(xmin,xmax, self.K + 1)
        self.centres= (gran[:-1] + gran[1:])/2
        self.step = (xmax - xmin)/ self.K
        quantized = []
        for x in time_series:
            i = int((x - xmin) / self.step)
            if i < 0:
                i = 0
            elif i >= self.K:
                i = self.K - 1
            quantized.append(i)
        c= self.huffman.encode(quantized)
        return c



    def decompress(self, bits: str) -> NDArrayFloat:
        indx= self.huffman.decode(bits)
        decompressed = []
        for i in indx:
            decompressed.append(self.centres[i])
        return np.array(decompressed)


if __name__ == "__main__":
    ts = np.loadtxt("ts_homework_practicum_5.txt")

    compressor = LossyCompression()
    bits = compressor.compress(ts)
    decompressed_ts = compressor.decompress(bits)

    compression_ratio = (len(ts) * 32 * 8) / len(bits) 
    print(f"Compression ratio: {compression_ratio:.2f}")

    compression_loss = np.sqrt(np.mean((ts - decompressed_ts)**2))
    print(f"Compression loss (RMSE): {compression_loss}")

