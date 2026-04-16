from pathlib import Path
import heapq
from typing import Any
from abc import ABC, abstractmethod

import networkx as nx
import numpy as np

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph, NDArrayFloat

class HuffmanCoding:

    class Node:

        def __init__(self, frequency, number = None, left = None, right = None):
            self.frequency = frequency
            self.number = number
            self.left = left
            self.right = right

        def __lt__(self, other):
            return self.frequency < other.frequency

    def __init__(self) -> None:

        self.codes = {}
        self.decoding_codes = {}
        self.tree_root = None

    def build_tree(self, number_list):

        frequency = {}
        for num in number_list:
            frequency[num] = frequency.get(num, 0) + 1

        heap = []
        for n, f in frequency.items():
            heap.append(self.Node(f, number = n))
        heapq.heapify(heap)

        while len(heap) > 1:
            n1 = heapq.heappop(heap)
            n2 = heapq.heappop(heap)
            merge_2nodes = self.Node(n1.frequency + n2.frequency, left = n1, right = n2)
            heapq.heappush(heap, merge_2nodes)
        self.tree_root = heap[0]

    def code_num(self, node, pathtoNode = ""):

        if node is None:
            return

        if node.number is not None:
            self.codes[node.number] = pathtoNode
            self.decoding_codes[pathtoNode] = node.number
            return

        self.code_num(node.left, pathtoNode + "0")
        self.code_num(node.right, pathtoNode + "1")
            
    def encode(self, sequence: list[Any]) -> str:

        self.codes = {}
        self.decoding_codes = {}
        
        self.build_tree(sequence)
        self.code_num(self.tree_root)

        encoded_tree = ""
        for num in sequence:
            encoded_tree += self.codes[num]

        return encoded_tree
        
    def decode(self, encoded_sequence: str) -> list[Any]:

        decoded_tree = []
        current_node = self.tree_root

        for bit  in encoded_sequence:
            if bit == "0":
                current_node = current_node.left
            else:
                current_node = current_node.right

            if current_node.number is not None:
                decoded_tree.append(current_node.number)
                current_node = self.tree_root

        return decoded_tree

class LossyCompression:

    def __init__(self) -> None:
        
        self.compression_levels = 16
        self.min_val = None
        self.max_val = None
        self.huffman = HuffmanCoding()

    def quantize(self, data):

        self.min_val = np.min(data)
        self.max_val = np.max(data)

        K = self.compression_levels
        z = np.linspace(self.min_val, self.max_val, K + 1)
        centers = (z[:-1] + z[1:]) / 2

        interval = np.digitize(data, z) - 1
        interval = np.clip(interval, 0, K - 1)

        quantized = centers[interval]

        return quantized
        
    def compress(self, time_series: NDArrayFloat) -> str:

        time_series = np.asarray(time_series)
        quantized = self.quantize(time_series)
        bits = self.huffman.encode(quantized.tolist())

        return bits

    def decompress(self, bits: str) -> NDArrayFloat:

        decoded = self.huffman.decode(bits)

        return np.array(decoded)


if __name__ == "__main__":
    ts = np.loadtxt("ts_homework_practicum_5.txt")

    compressor = LossyCompression()
    bits = compressor.compress(ts)
    decompressed_ts = compressor.decompress(bits)

    compression_ratio = (len(ts) * 32 * 8) / len(bits) 
    print(f"Compression ratio: {compression_ratio:.2f}")

    compression_loss = np.sqrt(np.mean((ts - decompressed_ts)**2))
    print(f"Compression loss (RMSE): {compression_loss}")

