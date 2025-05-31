from pathlib import Path
import heapq
from typing import Any
from abc import ABC, abstractmethod
import collections

import networkx as nx
import numpy as np

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph, NDArrayFloat


class HuffmanCoding:
    def __init__(self) -> None:
        self.encoding_table = {}
        self.tree_root = None

    def encode(self, sequence: list[Any]) -> str:
        frequencies = collections.Counter(sequence)
        heap = [[weight, [symbol, ""]] for symbol, weight in frequencies.items()]
        heapq.heapify(heap)

        # Построение дерева Хаффмана
        while len(heap) > 1:
            lo = heapq.heappop(heap)
            hi = heapq.heappop(heap)
            for pair in lo[1:]:
                pair[1] = '0' + pair[1]
            for pair in hi[1:]:
                pair[1] = '1' + pair[1]
            heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
        
        # Формирование таблицы кодов
        self.tree_root = heap[0]
        for p in self.tree_root[1:]:
            self.encoding_table[p[0]] = p[1]
        
        # Кодирование входной последовательности
        return ''.join([self.encoding_table[symb] for symb in sequence])
        

    def decode(self, encoded_sequence: str) -> list[Any]:       
        # Декодировать битовую строку
        result = []
        current_node = self.tree_root
        for bit in encoded_sequence:
            index = 1 if bit == '1' else 0
            next_nodes = current_node[index+1:]
            if len(next_nodes) == 1:
                result.append(next_nodes[0][0])
                current_node = self.tree_root
            else:
                current_node = next_nodes
        return result

class LossyCompression:
    def __init__(self) -> None:
        self.huffman_coding = HuffmanCoding()

    def compress(self, time_series: NDArrayFloat) -> tuple[str, float, float]:
        # Нормализовать и заквантизировать временной ряд
        min_val = time_series.min()
        max_val = time_series.max()
        normalized_values = (time_series - min_val) / (max_val - min_val)
        quantized_values = np.round(normalized_values * 255).astype(int)
        # Применить Хаффмановское кодирование
        huffman_bits = self.huffman_coding.encode(list(quantized_values))
        
        return huffman_bits, min_val, max_val

    def decompress(self, compressed_data: tuple[str, float, float]) -> NDArrayFloat:
        # Распаковка данных
        bits, min_val, max_val = compressed_data
        # Декодировка хаффмановской строки
        decoded_quantized_values = self.huffman_coding.decode(bits)
        # Обратное преобразование нормализованного диапазона
        denormalized_values = np.array(decoded_quantized_values) / 255 * (max_val - min_val) + min_val
        return denormalized_values

if __name__ == "__main__":
    ts = np.loadtxt("ts_homework_practicum_5.txt")

    compressor = LossyCompression()
    bits = compressor.compress(ts)
    decompressed_ts = compressor.decompress(bits)

    compression_ratio = (len(ts) * 32 * 8) / len(bits) 
    print(f"Compression ratio: {compression_ratio:.2f}")

    compression_loss = np.sqrt(np.mean((ts - decompressed_ts)**2))
    print(f"Compression loss (RMSE): {compression_loss}")

