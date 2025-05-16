from pathlib import Path
import heapq
from typing import Any
from abc import ABC, abstractmethod
from sys import getsizeof

import networkx as nx
import numpy as np

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph, NDArrayFloat


class HuffmanCoding:
    def __init__(self) -> None:
        codes = dict()

    def encode(self, sequence: list[Any]) -> str:
        frequency = {}
        for item in sequence:
            if item not in frequency:
                frequency[item] = 0
            frequency[item] += 1
        heap = [[weight, [item, ""]] for item, weight in frequency.items()]
        while len(heap) > 1:
            lo = heapq.heappop(heap)
            hi = heapq.heappop(heap)
            for pair in lo[1:]:
                pair[1] = '0' + pair[1]
            for pair in hi[1:]:
                pair[1] = '1' + pair[1]
            heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
        self.codes = dict(heap[0][1:])

    def decode(self, encoded_sequence: str) -> list[Any]:

        ##########################
        ### PUT YOUR CODE HERE ###
        ##########################

        pass


class LossyCompression:
    def __init__(self) -> None:
        self.coder = HuffmanCoding()
        self.scale = 0
        self.zero_point = 0

    def compress(self, time_series: NDArrayFloat) -> str:
        rmin, rmax = min(time_series), max(time_series)
        qmin, qmax = 0, 255
        self.scale = (rmax - rmin) / (qmax - qmin)
        self.zero_point = qmin - round(rmin/self.scale)

        quantized_values = [round(elem/self.scale) + self.zero_point for elem in time_series]
        self.coder.encode(quantized_values)
        resulted_code = ""
        for i in quantized_values:
            resulted_code += self.coder.codes[i]
        return resulted_code
        


    def decompress(self, bits: str) -> NDArrayFloat:
        quantized_values = []
        temp = ""
        for bit in bits:
            temp += bit
            for value, code in self.coder.codes.items():
                if temp == code:
                    quantized_values.append(value)
                    temp = ""
                    break
        dequantized_values = [(value-self.zero_point)*self.scale for value in quantized_values]
        return np.array(dequantized_values, dtype=np.float64)


if __name__ == "__main__":
    ts = np.loadtxt("ts_homework_practicum_5.txt")
    
    # coder = HuffmanCoding()
    # coder.encode([1, 2, 3, 4, 4, 4, 4, 5, 5, 6])
    # print(coder.codes)

    compressor = LossyCompression()
    bits = compressor.compress(ts)
    decompressed_ts = compressor.decompress(bits)

    compression_ratio = (len(ts) * 32 * 8) / len(bits) 
    print(f"Compression ratio: {compression_ratio:.2f}")

    compression_loss = np.sqrt(np.mean((ts - decompressed_ts)**2))
    print(f"Compression loss (RMSE): {compression_loss}")

