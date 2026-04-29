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

        ##########################
        ### PUT YOUR CODE HERE ###
        ##########################

        pass

    def compress(self, time_series: NDArrayFloat) -> str:

        ##########################
        ### PUT YOUR CODE HERE ###
        ##########################

        pass

    def decompress(self, bits: str) -> NDArrayFloat:

        ##########################
        ### PUT YOUR CODE HERE ###
        ##########################

        pass


if __name__ == "__main__":
    ts = np.loadtxt("ts_homework_practicum_5.txt")

    compressor = LossyCompression()
    bits = compressor.compress(ts)
    decompressed_ts = compressor.decompress(bits)

    compression_ratio = (len(ts) * 32 * 8) / len(bits) 
    print(f"Compression ratio: {compression_ratio:.2f}")

    compression_loss = np.sqrt(np.mean((ts - decompressed_ts)**2))
    print(f"Compression loss (RMSE): {compression_loss}")

