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
        self.res = {el: '' for el in sequence}
        self.decode_res = {el: '' for el in sequence}

        for el in sequence:
            self.freq[el] += 1

        for i in range(len(self.freq) - 1):
            min_v1 = min(self.freq.values())
            min1 = min(self.freq, key=self.freq.get)
            del self.freq[min1]
            min_v2 = min(self.freq.values())
            min2 = min(self.freq, key=self.freq.get)
            del self.freq[min2]

            for el_of_min1 in min1:
                self.res[el_of_min1] = '0' + self.res[el_of_min1]
            for el_of_min2 in min2:
                self.res[el_of_min2] = '1' + self.res[el_of_min2]

            self.freq[min1 + min2] = min_v1 + min_v2

        code = ''
        for el in sequence:
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

        self.intervals = []
        self.centers = []
        self.code = None

    def compress(self, time_series: NDArrayFloat) -> str:

        self.len = len(time_series)
        self.min = np.min(time_series)
        self.max = np.max(time_series)
        self.interval_len = (max(time_series) - min(time_series)) / len(time_series)
        self.intervals = [np.min(time_series)]

        for k in range(self.len):
            self.intervals.append(self.intervals[-1] + self.interval_len)
            self.centers.append((self.intervals[-2] + self.intervals[-1]) / 2)
        self.code = np.digitize(time_series, bins=self.intervals) - 1
        code = '_'.join(map(str, self.code))
        return code

    def decompress(self, bits: str) -> NDArrayFloat:
        i = 0
        s = ''
        ind = []
        while i < len(bits):
            if bits[i] != '_':
                s += bits[i]
            else:
                ind.append(int(s))
                s = ''
            i += 1
        ind.append(int(s))
        res = [self.centers[i] for i in ind]
        return np.array(res, dtype=np.float64)

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
