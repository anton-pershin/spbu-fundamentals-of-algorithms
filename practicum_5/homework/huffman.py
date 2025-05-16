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

        ##########################
        ### PUT YOUR CODE HERE ###
        ##########################

        pass

    def encode(self, sequence: list[Any]) -> str:

        ##########################
        ### PUT YOUR CODE HERE ###
        ##########################

        pass
        

    def decode(self, encoded_sequence: str) -> list[Any]:

        ##########################
        ### PUT YOUR CODE HERE ###
        ##########################

        pass


class LossyCompression:
    def __init__(self) -> None:
        self.n = 8
        self.min_value = None
        self.max_value = None
        self.edges = None
        self.centers = None

    def compress(self, time_series: NDArrayFloat) -> str:
        self.min_value = np.min(time_series)
        self.max_value = np.max(time_series)
        self.edges = np.linspace(self.min_value, self.max_value, self.n + 1)
        self.centers = (self.edges[:-1] + self.edges[1:]) / 2

        indices = np.digitize(time_series, self.edges[1:-1], right=True)
        bits_per_symbol = int(np.ceil(np.log2(self.n)))
        bits = ''.join([format(idx, f'0{bits_per_symbol}b') for idx in indices])
        return bits
        
    def decompress(self, bits: str) -> NDArrayFloat:
        bits_per_symbol = int(np.ceil(np.log2(self.n)))
        indices = [int(bits[i:i+bits_per_symbol], 2) 
                  for i in range(0, len(bits), bits_per_symbol)]
        indices = np.clip(indices, 0, len(self.centers)-1)
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

