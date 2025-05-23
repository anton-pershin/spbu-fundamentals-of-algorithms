import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

import heapq
from typing import Any, Dict, List, Tuple
from abc import ABC, abstractmethod

import networkx as nx
import numpy as np

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph, NDArrayFloat


class HuffmanCoding:
    def __init__(self) -> None:
        # Словарь: символ → его код Хаффмана
        self.codes: Dict[Any, str] = {}
        # Словарь обратный: код → символ для декодирования
        self.reverse_codes: Dict[str, Any] = {}
        # Корень дерева в виде кортежа (symbol, left, right)
        self.root: Tuple[Any, Any, Any] = None

    def encode(self, sequence: list[Any]) -> str:
        # 1. Подсчитаем частоты символов
        counts: Dict[Any, int] = {}
        for x in sequence:
            counts[x] = counts.get(x, 0) + 1

        # 2. Построим кучу из кортежей (freq, counter, node)
        heap: List[Tuple[int, int, Tuple[Any, Any, Any]]] = []
        counter = 0
        for sym, freq in counts.items():
            # node: (symbol, left, right)
            heapq.heappush(heap, (freq, counter, (sym, None, None)))
            counter += 1

        # Случай для одного символа
        if len(heap) == 1:
            _, _, leaf = heap[0]
            self.root = (None, leaf, None)
        else:
            # 3. Объединим два узла с наименьшей частотой, пока не останется один
            while len(heap) > 1:
                f1, c1, n1 = heapq.heappop(heap)
                f2, c2, n2 = heapq.heappop(heap)
                merged = (None, n1, n2)
                heapq.heappush(heap, (f1 + f2, counter, merged))
                counter += 1
            # Если остался корень
            _, _, self.root = heap[0]

        # 4. Строим словари кодирования
        self.codes.clear()
        self.reverse_codes.clear()

        def traverse(node: Tuple[Any, Any, Any], prefix: str) -> None:
            symbol, left, right = node
            if symbol is not None:
                code = prefix or '0'
                self.codes[symbol] = code
                self.reverse_codes[code] = symbol
            else:
                # "0" - шаг влево, "1" - шаг вправо
                if left is not None:
                    traverse(left, prefix + '0')
                if right is not None:
                    traverse(right, prefix + '1')

        traverse(self.root, '')

        # 5. Закодировать входные данные
        return ''.join(self.codes[x] for x in sequence)

    def decode(self, encoded_sequence: str) -> list[Any]:
        if self.root is None:
            return []
        result: List[Any] = []
        node = self.root
        for bit in encoded_sequence:
            symbol, left, right = node
            # переход по дереву
            node = left if bit == '0' else right
            sym, l, r = node
            if sym is not None:
                # если лист — добавить символ и сбросить на корень
                result.append(sym)
                node = self.root
        return result

class LossyCompression:
    def __init__(self, num_levels: int = 16) -> None:
        # Число уровней квантования
        self.num_levels = num_levels
        # Параметры квантования
        self._min: float = 0.0
        self._max: float = 0.0
        self._levels: np.ndarray = np.array([])
        # Объект класса HuffmanCoding
        self._huffman: HuffmanCoding = None

    def compress(self, time_series: NDArrayFloat) -> str:
        # Квантование данных на num_levels уровней
        # и Хаффман-кодирование полученный индексов
        # Результат - побитовая строка

        # Находим диапазон
        self._min, self._max = float(time_series.min()), float(time_series.max())
        self._levels = np.linspace(self._min, self._max, self.num_levels)

        # Квантование: от 0 до num_levels-1
        normalized = (time_series - self._min) / (self._max - self._min) * (self.num_levels - 1)
        indices = np.rint(normalized).astype(int)
        seq = indices.tolist()

        # Хаффман-кодирование индексов
        self._huffman = HuffmanCoding()
        bits = self._huffman.encode(seq)
        return bits

    def decompress(self, bits: str) -> NDArrayFloat:
        # Раскодируем биты в последовательность индексов,
        # затем сопоставим индексы с уровнями квантования.
        # Результат - восстановленный массив
        indices = self._huffman.decode(bits)
        levels = self._levels
        indices = np.clip(indices, 0, len(levels) - 1)
        reconstructed = levels[indices]
        return reconstructed

if __name__ == "__main__":
    ts = np.loadtxt(project_root / "practicum_5" / "homework" / "ts_homework_practicum_5.txt")

    compressor = LossyCompression()
    bits = compressor.compress(ts)
    decompressed_ts = compressor.decompress(bits)

    compression_ratio = (len(ts) * 32 * 8) / len(bits) 
    print(f"Compression ratio: {compression_ratio:.2f}")

    compression_loss = np.sqrt(np.mean((ts - decompressed_ts)**2))
    print(f"Compression loss (RMSE): {compression_loss}")

