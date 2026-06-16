from pathlib import Path
import heapq
from typing import Any
from abc import ABC, abstractmethod

import networkx as nx
import numpy as np

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph, NDArrayFloat
from collections import Counter


class HuffmanCoding:
    def __init__(self) -> None:
        self.freq = {}
        self.codes = {}
        self.reverse_codes = {}

    def encode(self, sequence: list[Any]) -> str:
        self.freq = Counter(sequence)
        heap = []
        for key,val in self.freq.items():
            heapq.heappush(heap,(val,key,None,None))

        huffmanTree = self._createTree(heap)
        self._getCodes(huffmanTree,"")
        
        encodedString = "".join(self.codes[symbol] for symbol in sequence)
        return encodedString


    def _getCodes(self,node : tuple,curCode : str) -> None:
        freq,val,left,right = node

        if (val != -1):
            self.codes[val] = curCode;
            self.reverse_codes[curCode] = val
            return
        if left:
            self._getCodes(left,curCode + "0")
        if right:
            self._getCodes(right,curCode + "1")
    

    def _createTree(self,heap : list[Any]) -> tuple:
        while (len(heap) > 1):
            node1 = heapq.heappop(heap)
            node2 = heapq.heappop(heap)

            comb_freq = node1[0] + node2[0]
            parent = (comb_freq,-1,node1,node2)

            heapq.heappush(heap,parent)
        return heap[0]


    def decode(self, encoded_sequence: str) -> list[Any]:
        code = ""
        decoded = []
        for i in encoded_sequence:
            code += i
            if (code in self.reverse_codes):
                decoded.append(self.reverse_codes[code])
                code = ""
        return decoded

class LossyCompression:
    def __init__(self) -> None:
        # variable parameter k, for example there k=64
        self.k = 64
        self.huffman = HuffmanCoding()
        self.centers = []

    def compress(self, time_series: NDArrayFloat) -> str:
        self.mini = time_series.min()
        self.maxi = time_series.max()

        step = (self.maxi - self.mini) / self.k
        halfStep = step / 2
        self.centers = np.linspace(self.mini +halfStep, self.maxi-halfStep,self.k)
    
        bins = np.linspace(self.mini,self.maxi,self.k+1)
        q_indices = np.digitize(time_series,bins) - 1;
        q_indices = np.clip(q_indices,0,self.k-1)

        result = self.huffman.encode(q_indices)
       
        return result

    def decompress(self, bits: str) -> NDArrayFloat:
        indices = self.huffman.decode(bits);

        return self.centers[indices]


if __name__ == "__main__":
    ts = np.loadtxt("ts_homework_practicum_5.txt")

    compressor = LossyCompression()
    bits = compressor.compress(ts)
    decompressed_ts = compressor.decompress(bits)

    compression_ratio = (len(ts) * 32 * 8) / len(bits) 
    print(f"Compression ratio: {compression_ratio:.2f}")

    compression_loss = np.sqrt(np.mean((ts - decompressed_ts)**2))
    print(f"Compression loss (RMSE): {compression_loss}")

