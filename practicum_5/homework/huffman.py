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

        self.codes={}

        pass

    def build_codes(self,node,code):

        if isinstance(node,str):
            self.codes[node]=code
            return
        left_child=node[0]
        right_child=node[1]
        self.build_codes(left_child, code + '0')
        self.build_codes(right_child, code + '1')
    def encode(self, sequence: list[Any]) -> str:
        count={}
        for s in sequence:
            if s in count:
                count[s]+=1
            else:
                count[s]=1
        heap=[]
        counter=0
        for s,kol in count.items():
            heapq.heappush(heap,(kol,counter,s))
            counter+=1

        while len(heap)>1:
            k1,c1,first=heapq.heappop(heap)
            k2,c2, second=heapq.heappop(heap)
            new_k=k1+k2
            heapq.heappush(heap,(new_k,counter,(first,second)))
            counter+=1

        root_k,_,root_node=heap[0]
        self.build_codes(root_node,"")

        result=""
        for s in sequence:
            result=result+self.codes[s]

        return result

        pass


    def decode(self, encoded_sequence: str) -> list[Any]:

        revers_codes={}
        for s,code in self.codes.items():
            revers_codes[code]=s
        current_code=""
        result=[]
        for bit in encoded_sequence:
            current_code+=bit
            if current_code in revers_codes:
                result.append(revers_codes[current_code])
                current_code=""

        return result

        pass


class LossyCompression:
    def __init__(self) -> None:

        self.K=64
        self.huffman = HuffmanCoding()

        pass

    def compress(self, time_series: NDArrayFloat) -> str:

        min_num=min(time_series)
        max_num=max(time_series)
        step=(max_num-min_num)/self.K
        boundaries=[]
        for i in range(self.K + 1):
            boundaries.append(min_num + i * step)
        centers=[]
        for i in range(self.K):
            first_bound=boundaries[i]
            second_bound=boundaries[i+1]
            centers.append((first_bound+second_bound)/2)
        new_num=[]
        for num in time_series:
            ind=0
            for i in range(self.K):
                if i == (self.K - 1):
                    if boundaries[i] <= num <= boundaries[i + 1]:
                        ind = i
                        break
                else:
                    if boundaries[i] <= num < boundaries[i + 1]:
                        ind = i
                        break
            new_num.append(centers[ind])

        symbols = [str(v) for v in new_num]
        bits = self.huffman.encode(symbols)

        return bits

        pass

    def decompress(self, bits: str) -> NDArrayFloat:

        symbols= self.huffman.decode(bits)
        result=[float(s) for s in symbols]
        return result
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

