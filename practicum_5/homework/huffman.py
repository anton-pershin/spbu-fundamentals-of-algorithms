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
        self.huf = {}
        self.meaning = {}        

    def encode(self, sequence: list[Any]) -> str:
        if not sequence:
            return ""
        
        list_count = {}
        for num in sequence:
            if num in list_count:
                list_count[num] += 1
            else:
                list_count[num] = 1
        
        queue = [[count, num] for num, count in list_count.items()]
        heapq.heapify(queue)

        self.huf = {}
        self.meaning = {}

        if len(queue) == 1:
            numeral = queue[0][1]
            self.huf[numeral] = "0"
            self.meaning["0"] = numeral
        else:
            while len(queue) > 1:
                left = heapq.heappop(queue)
                right = heapq.heappop(queue)
                new_node = [left[0] + right[0], left, right]
                heapq.heappush(queue, new_node)

            def huf_code (node: Any, current: str) -> None:
                if len(node) == 2:
                    self.huf[node[1]] = current
                    self.meaning[current] = node[1]
                else:
                    huf_code(node[1], current + "0")
                    huf_code(node[2], current + "1")
            
            huf_code(queue[0], "")

        result = ""
        for num in sequence:
            result += self.huf[num]
        return result

    def decode(self, encoded_sequence: str) -> list[Any]:
        result = []
        current = ""

        for i in encoded_sequence:
            current += i

            if current in self.meaning:
                numeral = self.meaning[current]
                result.append(numeral)
                current = ""
        
        return result


class LossyCompression:
    def __init__(self) -> None:
        self.intervals = 16
        self.step = 0.0
        self.centres = []
        self.huffman = HuffmanCoding()

    def compress(self, time_series: NDArrayFloat) -> str:
        min_num = time_series.min()
        max_num = time_series.max()

        if max_num == min_num:
            self.step = 0.0
            self.centres = [min_num]
            quantized = [0] * len(time_series)
        else:
            self.step = (max_num - min_num) / self.intervals
            self.centres = [min_num + self.step * (i + 0.5) for i in range(self.intervals)]
            
            quantized = []
            for j in time_series:
                index = int((j - min_num) / self.step)
                if index < 0:
                    index = 0
                if index >= self.intervals:
                    index = self.intervals - 1
                quantized.append(index)
    
        return self.huffman.encode(quantized)

    def decompress(self, bits: str) -> NDArrayFloat:
        decoded = self.huffman.decode(bits)
        return np.array([self.centres[i] for i in decoded])


if __name__ == "__main__":
    ts = np.loadtxt("ts_homework_practicum_5.txt")

    compressor = LossyCompression()
    bits = compressor.compress(ts)
    decompressed_ts = compressor.decompress(bits)

    compression_ratio = (len(ts) * 32 * 8) / len(bits) 
    print(f"Compression ratio: {compression_ratio:.2f}")

    compression_loss = np.sqrt(np.mean((ts - decompressed_ts)**2))
    print(f"Compression loss (RMSE): {compression_loss}")

