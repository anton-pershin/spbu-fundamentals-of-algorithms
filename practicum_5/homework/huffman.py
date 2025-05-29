from pathlib import Path
import heapq
from typing import Any
from abc import ABC, abstractmethod


import networkx as nx
import numpy as np
from scipy.spatial.distance import seuclidean

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph, NDArrayFloat


class HuffmanCoding:
    def __init__(self) -> None:
        self.freq = {}
        self.res = {}
        self.decode_res = {}
        self.in_code = []

    def encode(self, sequence: list[Any]) -> str:

        self.freq = {el: 0 for el in sequence}
        self.res = {str(el): '' for el in sequence}
        self.decode_res = {str(el): '' for el in sequence}

        for el in sequence:
            self.freq[el] += 1

        for i in range(len(self.freq) - 1):
            min_v1 = min(self.freq.values())
            min1 = min(self.freq, key=self.freq.get)
            del self.freq[min1]
            min_v2 = min(self.freq.values())
            min2 = min(self.freq, key=self.freq.get)
            del self.freq[min2]

            min1 = str(min1)
            min2 = str(min2)
            i = 0
            s = ''
            while i < len(min1):
                if min1[i] == '_':
                    if s in self.res:
                        self.res[s] = '0' + self.res[s]
                    else:
                        self.res[s] = '0'
                    s = ''
                else:
                    s += min1[i]
                i += 1
            if s in self.res:
                self.res[s] = '0' + self.res[s]
            else:
                self.res[s] = '0'

            i = 0
            s = ''
            while i < len(min2):
                if min2[i] == '_':
                    if s in self.res:
                        self.res[s] = '1' + self.res[s]
                    else:
                        self.res[s] = '1'
                    s = ''
                else:
                    s += min2[i]
                i += 1
            if s in self.res:
                self.res[s] = '1' + self.res[s]
            else:
                self.res[s] = '1'

            self.freq[min1 + '_' + min2] = min_v1 + min_v2

        code = ''
        for el in sequence:
            el = str(el)
            code += self.res[el]
            self.in_code.append(self.res[el])
            self.decode_res[self.res[el]] = el

        return code

    def decode(self, encoded_sequence: str) -> list[Any]:
        s = ''
        decode = []

        for el in encoded_sequence:
            s += el
            if s in self.in_code:
                decode.append(self.decode_res[s])
                s = ''

        return decode


class LossyCompression:
    def __init__(self) -> None:
        self.huffman = HuffmanCoding()
        self.code = None
        self.min = None
        self.max = None

    def compress(self, time_series: NDArrayFloat) -> str:
        self.min = np.min(time_series)
        self.max = np.max(time_series)

        quantized = [
            int(((x - self.min) / (self.max - self.min)) * (2 ** 4 - 1))
            for x in time_series
        ]

        return self.huffman.encode(quantized)

    def decompress(self, bits: str) -> NDArrayFloat:
        quantized = np.array(self.huffman.decode(bits), dtype=np.float32)
        normalized = quantized / (2 ** 4 - 1)

        return normalized * (self.max - self.min) + self.min

if __name__ == "__main__":
    ts1 = np.loadtxt("ts_homework_practicum_5.txt")

    compressor = LossyCompression()
    bits = compressor.compress(ts1)

    decompressed_ts = compressor.decompress(bits)

    compression_ratio = (len(ts1) * 32 * 8) / len(bits)
    print(f"Compression ratio: {compression_ratio:.2f}")

    compression_loss = np.sqrt(np.mean((ts1 - decompressed_ts)**2))
    print(f"Compression loss (RMSE): {compression_loss}")

    huffman = HuffmanCoding()
    data = ['a', 'b', 'a', 'c']
    encoded_data = huffman.encode(data)
    print("Code for data:", encoded_data)

    decoded_data = huffman.decode(encoded_data)
    print("Decoded data:", decoded_data)
