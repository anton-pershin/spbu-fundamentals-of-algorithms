from pathlib import Path
import heapq as hq
from typing import Any
from abc import ABC, abstractmethod
from collections import Counter

import networkx as nx
import numpy as np

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph, NDArrayFloat

# Node class for HuffmanTree
class Node:
    def __init__(self, freq, number = 0, left = None, right = None):
        self.freq = freq
        self.number = number
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

    def __repr__(self):
        return f"Number: {self.number}\n {self.freq}\nIncludes:\n {self.left}\n {self.right}\n(End of {self.number} includes)"

# Tree for HuffmanEncoding
class HuffmanTree:
    def __init__(self):
        self.tree = None
            
    def build(self, sequence: list[Any]) -> None:
        # Making a list of single-noded trees
        freqs = Counter(sequence)
        forest = [Node(freq, number) for number, freq in freqs.items()]

        # Making a heap out of trees
        hq.heapify(forest)
            
        # Building a tree according to Huffman Algorithm
        while len(forest) > 1:
            left = hq.heappop(forest)
            right = hq.heappop(forest)

            connector = Node(left.freq + right.freq, 0, left, right)

            hq.heappush(forest, connector)
        
        # Assigning the tree to the object
        self.tree = forest[0]

    # Simple dfs with path fixation for getAlphabet()
    def dfs(self, node: Node, curCode: str, alphabet: dict()) -> dict():
        if (not node.left and not node.right):
            alphabet[node.number] = curCode

        if node.left:
            self.dfs(node.left, curCode + "0", alphabet)
        if node.right:
            self.dfs(node.right, curCode + "1", alphabet)

        return alphabet
    
    # Get an alphabet in format (number, code)
    def getAlphabet(self) -> dict():
        alphabet = self.dfs(self.tree, "", {})
        return alphabet
    
# Coding for the LossyCompression
class HuffmanCoding:
    def __init__(self) -> None:
        self.tree = None

    def encode(self, sequence: list[Any]) -> str:
        self.tree = HuffmanTree()
        self.tree.build(sequence)
        alphabet = self.tree.getAlphabet()

        encoded = str()
        for number in sequence:
            encoded += alphabet[number]

        print(alphabet)
        return encoded


    def decode(self, encoded_sequence: str) -> list[Any]:
        if self.tree == None: raise Exception("Haven't encoded anything yet!")
        alphabet = self.tree.getAlphabet()
        # getAlphabet returns (number, code) format so we have to invert it to decode
        alphabet = {code : number for number, code in alphabet.items()}
    
        decoded = list()
        buffer = str()
        for bit in encoded_sequence:
            buffer += bit
            if buffer in alphabet:
                decoded.append(alphabet[buffer])
                buffer = ""
        
        return decoded

class LossyCompression:
    def __init__(self) -> None:
        self.coder = HuffmanCoding()
    
    # This part of the code is a bit clumsy, I'm sorry :c
    def compress(self, time_series: NDArrayFloat) -> str:        
        minim = np.min(time_series)
        maxim = np.max(time_series)
        # I didn't know what K must be exactly and got a bit afraid to ask
        # So i supposed it is a quantity of unique numbers in the time series
        # It may be changed as you like
        capacity = len(set(time_series))
        
        diff = (maxim - minim) / capacity

        intervals = list()
        down = minim
        while down < maxim:
            intervals.append((down, down + diff))
            down += diff
        # In case of too small or imprecise diff
        if 0 < maxim - intervals[-1][1] < diff:
            intervals[-1] = (intervals[-1][0], maxim)

        approx = [float((up + down)/2) for down, up in intervals]
        
        sequence = list()
        for number in time_series:
            for i in range(len(intervals)):
                down = intervals[i][0]
                up = intervals[i][1]
                if down <= number <= up:
                    sequence.append(approx[i])
                    break

        encoded = self.coder.encode(sequence)

        return encoded

    def decompress(self, bits: str) -> NDArrayFloat:
        decoded = self.coder.decode(bits)
        npArray = np.array(decoded, dtype=np.float64)
        return npArray

if __name__ == "__main__":
    ts = np.loadtxt("ts_homework_practicum_5.txt")

    compressor = LossyCompression()
    bits = compressor.compress(ts)
    decompressed_ts = compressor.decompress(bits)

    compression_ratio = (len(ts) * 32 * 8) / len(bits) 
    print(f"Compression ratio: {compression_ratio:.2f}")

    compression_loss = np.sqrt(np.mean((ts - decompressed_ts)**2))
    print(f"Compression loss (RMSE): {compression_loss}")

