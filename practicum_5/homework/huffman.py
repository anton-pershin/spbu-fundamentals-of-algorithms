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

# Personal test
if __name__ == "__main__":
    l1 = [1, 2, 3, 3, 4, 2, 5]
    l2 = [6, 6, 7, 9, 0, 8]
    
    coder1 = HuffmanCoding()
    coder2 = HuffmanCoding()
    
    coded1 = coder1.encode(l1)
    coded2 = coder2.encode(l2)
    
    decoded1 = coder1.decode(coded1)
    decoded2 = coder2.decode(coded2)
    
    print(coded1, decoded1)
    print(coded2, decoded2)

    coder1.decode(coded2)

#if __name__ == "__main__":
#    ts = np.loadtxt("ts_homework_practicum_5.txt")
#
#    compressor = LossyCompression()
#    bits = compressor.compress(ts)
#    decompressed_ts = compressor.decompress(bits)
#
#    compression_ratio = (len(ts) * 32 * 8) / len(bits) 
#    print(f"Compression ratio: {compression_ratio:.2f}")
#
#    compression_loss = np.sqrt(np.mean((ts - decompressed_ts)**2))
#    print(f"Compression loss (RMSE): {compression_loss}")

