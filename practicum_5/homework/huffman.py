from pathlib import Path
import heapq
from typing import Any
from abc import ABC, abstractmethod
from collections import Counter

import networkx as nx
import numpy as np

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph, NDArrayFloat


class HuffmanCoding:
    def __init__(self) -> None:
        self.G = None
        self.codes = dict()
        self.codes_inverse = dict()

    def encode(self, sequence: list[Any]) -> str:

        self.G = nx.Graph()
        word_counter = Counter(sequence)

        for key, count in word_counter.items():
            self.G.add_node(key, weight=count, target=True)

        queue = []
        counter = 0
        for node, data in self.G.nodes(data=True):
            counter += 1
            heapq.heappush(queue, (data['weight'], (counter, node)))

        f = 0
        while len(queue) > 1:
            counter += 1
            first_weight, (_, first_node) = heapq.heappop(queue)
            second_weight, (_, second_node) = heapq.heappop(queue)

            new_node = f"node_{f}"
            new_weight = first_weight + second_weight
            self.G.add_node(new_node, weight=new_weight, target=False)

            self.G.add_edge(new_node, first_node, name='0')
            self.G.add_edge(new_node, second_node, name='1')

            heapq.heappush(queue, (new_weight, (counter, new_node)))
            f += 1
        _, (_, root_node) = queue[0]
        paths = nx.single_source_shortest_path(self.G, root_node)

        for node, path in paths.items():
            if not self.G.nodes[node].get('target', False):
                continue
            code = ''.join(self.G[path[i]][path[i + 1]]['name'] for i in range(len(path) - 1))
            self.codes[node] = code
            self.codes_inverse[code] = node

        return ''.join(self.codes[word] for word in sequence)


    def decode(self, encoded_sequence: str) -> list[Any]:

        result = []
        current = ''
        for bit in encoded_sequence:
            current += bit
            if current in self.codes_inverse:
                result.append(self.codes_inverse[current])
                current = ''
        return result


class LossyCompression:
    def __init__(self) -> None:
        self.seq_min = 0.0
        self.seq_max = 0.0
        self.HC = None

    def compress(self, time_series: NDArrayFloat) -> str:

        self.seq_max = max(time_series)
        self.seq_min = min(time_series)
        self.seq_size = len(time_series)

        step = (self.seq_max - self.seq_min) / self.seq_size
        intervaly = np.arange(self.seq_min, self.seq_max + step, step)

        values = [(intervaly[i] + intervaly[i + 1]) / 2 for i in range(len(intervaly) - 1)]

        d = {i: values[i] for i in range(len(values))}
        result = []

        for x in time_series:
            idx = int((x - self.seq_min) / step)
            idx = min(idx, len(values) - 1)
            result.append(d[idx])

        self.HC = HuffmanCoding()
        return self.HC.encode(result)


    def decompress(self, bits: str) -> NDArrayFloat:

        decoded = self.HC.decode(bits)
        return np.array(decoded, dtype=float)


if __name__ == "__main__":
    ts = np.loadtxt("ts_homework_practicum_5.txt")

    compressor = LossyCompression()
    bits = compressor.compress(ts)
    decompressed_ts = compressor.decompress(bits)

    compression_ratio = (len(ts) * 32 * 8) / len(bits) 
    print(f"Compression ratio: {compression_ratio:.2f}")

    compression_loss = np.sqrt(np.mean((ts - decompressed_ts)**2))
    print(f"Compression loss (RMSE): {compression_loss}")

