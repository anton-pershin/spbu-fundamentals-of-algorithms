import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from pathlib import Path
import heapq
from typing import Any, List
from abc import ABC, abstractmethod

import networkx as nx
import numpy as np

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph, NDArrayFloat

import random


class HuffmanCoding:
    def __init__(self) -> None:
        self.frequency = {}
        self.codes = {}
        self.decoded_map = {}
        self.code_list = []


    def encode(self, sequence: List[Any]) -> str:
        self.frequency = {element: 0 for element in sequence}
        self.codes = {element: '' for element in sequence}
        self.decoded_map = {element: '' for element in sequence}

        for element in sequence:
            self.frequency[element] += 1

        while len(self.frequency) > 1:
            least_freq = {
                'left': min(self.frequency, key=self.frequency.get),
                'left_freq': self.frequency.pop(min(self.frequency, key=self.frequency.get)),
                'right': min(self.frequency, key=self.frequency.get),
                'right_freq': self.frequency.pop(min(self.frequency, key=self.frequency.get)),
            }

            for char in least_freq['left']:
                self.codes[char] = '0' + self.codes[char]
            for char in least_freq['right']:
                self.codes[char] = '1' + self.codes[char]

            self.frequency[least_freq['left'] + least_freq['right']] = least_freq['left_freq'] + least_freq['right_freq']

        self.code_list = [self.codes[element] for element in sequence]
        self.decoder_dict = {self.codes[element]: element for element in sequence}
        # print(self.decoder_dict, ''.join(self.code_list), self.code_list)

        return ''.join(self.code_list)


    def decode(self, enc_data: str) -> list[Any]:
        curr_code = ''
        result = ''
        for char in enc_data:
            curr_code += char
            if curr_code in self.code_list:
                result += self.decoder_dict[curr_code]
                curr_code = ''

        return list(result)



class LossyCompression:
    def __init__(self) -> None:
        self.centers = []

    def compress(self, time_series: NDArrayFloat) -> str:
        self.data = time_series
        self.interval_length = (np.max(time_series) - np.min(time_series)) / len(time_series)
        self.intervals = [np.min(time_series)]

        for _ in range(len(time_series)):
            self.intervals.append(self.intervals[-1] + self.interval_length)
            self.centers.append((self.intervals[-2] + self.intervals[-1]) / 2)
        self.compressed_code = np.digitize(self.data, bins=self.intervals) - 1

        return ';'.join([str(inx) for inx in self.compressed_code])


    def decompress(self, bits: str) -> NDArrayFloat:
        indices = list([int(bit) for bit in bits.split(';')])

        return np.array([self.centers[i] for i in indices], dtype=np.float64)


if __name__ == "__main__":

    huffman = HuffmanCoding()
    data = list('abcaao')
    enc_data = huffman.encode(data)
    dec_data = huffman.decode(enc_data)

    print('\n==============[ HUFFMAN ALGORITHM OUTPUT ]==============')
    print(
       f'\nData:                    {data}              ',
       f'\nEncoded data:            {enc_data}          ',
       f'\nDecoded data:            {dec_data}          ',
       f'\nActual and decode equal: {data == dec_data}\n'
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



