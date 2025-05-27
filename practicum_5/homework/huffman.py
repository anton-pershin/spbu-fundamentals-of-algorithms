import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from pathlib import Path
import heapq
from typing import Any, List, Union
from abc import ABC, abstractmethod

import networkx as nx
import numpy as np

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph, NDArrayFloat

import random


class HuffmanCoding:
    def __init__(self) -> None:
        self.encode_dict = {}
        self.decode_dict = {}
        

    def encode(self, sequence: list[Any]) -> str:
        freq_dict = {elem: 0 for elem in sequence}
        for elem in sequence:
            freq_dict[elem] += 1

        heap = [[freq, [char, '']] for char, freq in freq_dict.items()]
        heapq.heapify(heap)

        while len(heap) > 1:
            left  = heapq.heappop(heap)  # left elems / subtrees with min frequency
            right = heapq.heappop(heap)  # right elems / ...

            for elem in left[1:]:
                elem[1] = '0' + elem[1]
            for elem in right[1:]:
                elem[1] = '1' + elem[1]
            heapq.heappush(heap, [left[0] + right[0]] + left[1:] + right[1:])  # forming new node like: [summed_freq, [freq1, code1], [freq2, code2], ...]

        heap = heap[0]  # before this, the heap was an array within an array
        for elem in heap[1:]:  # starting from 1 as the first elem is total frequency, which is just the length of sequence
            self.encode_dict[elem[0]] = elem[1]
            self.decode_dict[elem[1]] = elem[0]

        return ''.join(self.encode_dict[char] for char in sequence)
        

    def decode(self, encoded_sequence: str) -> list[Any]:
        decoded = []
        bits = ''
        for bit in encoded_sequence:
            bits += bit
            if bits in self.decode_dict:
                decoded.append(self.decode_dict[bits])
                bits = ''
        return decoded
        


class LossyCompression:
    def __init__(self) -> None:
        self.gaps = 1000
        self.huffman = HuffmanCoding()

    def compress(self, time_series: NDArrayFloat) -> str:
        min_val, max_val = np.min(time_series), np.max(time_series)
        self.edges = np.linspace(min_val, max_val, self.gaps + 1)
        self.centers = [(self.edges[i] + self.edges[i + 1]) / 2 for i in range(self.gaps + 1 - 1)]
        indices = np.digitize(time_series, self.edges) - 1  # indices of segments which values lie in (determined by comparing the value to the edges; '- 1' cuz we start indices at 0 :) )
        indices = np.clip(indices, 0, self.gaps - 1)  # handling outliers
        
        return self.huffman.encode(list(indices))

    
    def decompress(self, bits: str) -> NDArrayFloat:
        indices = self.huffman.decode(bits)

        return np.array([self.centers[ind] for ind in indices])



if __name__ == "__main__":

    huffman = HuffmanCoding()
    data = [1,3,4,2,32,3,4]
    enc_data = huffman.encode(data)
    dec_data = huffman.decode(enc_data)

    print('\n==============[ HUFFMAN ALGORITHM OUTPUT ]==============')
    print(
       f'\nData:                     {data}              ',
       f'\nEncoded data:             {enc_data}          ',
       f'\nDecoded data:             {dec_data}          ',
       f'\nActual and decoded equal: {data == dec_data}\n'
    )



    ts = np.loadtxt("ts_homework_practicum_5.txt")

    compressor = LossyCompression()
    bits = compressor.compress(ts)
    decompressed_ts = compressor.decompress(bits)

    print('\n============[ COMPRESSION ALGORITHM OUTPUT ]============\n')
    random_inds = [random.randint(0, len(bits)) for _ in range(5)]
    print('[ Preview of some compressed values ]')
    print('\n'.join([f'{ts[i]} -> {decompressed_ts[i]}' for i in range(5)]))

    compression_ratio = (len(ts) * 32 * 8) / len(bits) 
    print(f"\nCompression ratio:       {compression_ratio:.2f}")

    compression_loss = np.sqrt(np.mean((ts - decompressed_ts)**2))
    print(f"Compression loss (RMSE): {compression_loss}")



