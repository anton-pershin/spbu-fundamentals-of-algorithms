
#
# 1) Квантизация вещественных чисел (с потерями)
#
#    Точные значения теряются, но 
#     при большом K ошибка мала.
#
#    - Разделить диапазон [min, max] на K равных частей.
#    - Определить центры отрезков (алфавит для пользователя).
#    - Значения заменить индексами отрезков (api-флфавит).
#
# 2) Код Хаффмана
#
#    Работаем с целыми индексами [0, K-1] (алфавит).
#    Чем чаще встречается индекс – тем короче его код.
#
#    Построение дерева:
#
#     - Считаем частоту f каждого символа.
#     - Кладем все пары (f, символ) в мин-кучу.
#     - Пока в куче > 1 узла:
#        - Берем два узла с наименьшей частотой;
#        - Создаем родителя с частотой f1 + f2;
#        - Кладем родителя обратно в кучу.
#     - Последний узел в куче – корень дерева.
#
#    Присвоение кодов:
#
#      Обходим дерево рекурсивно: влево -> 0, вправо -> 1.
#      Код символа = путь от корня до его листа.
#
#    Декодирование:
#
#      Читаем биты и движемся по дереву от корня.
#      Достигли листа – выводим символ, идем от корня заново.
#      Так до конца битовой строки.
#


from pathlib import Path
import heapq
from collections import Counter
from typing import Any
from abc import ABC, abstractmethod

import networkx as nx
import numpy as np

from src.plotting.graphs import plot_graph
from src.common import AnyNxGraph, NDArrayFloat


class HuffmanCoding:


    def __init__(self) -> None:

        # ("internal", left, right)
        #   left  -> ("leaf", symbol)
        #   right -> ("leaf", symbol)
        self._tree: tuple | None = None
        self._code_table: dict[Any, str] = {}


    def encode(self, indices: list[Any]) -> str:

        # indices -> _tree + _code_table
        self._build_tree(indices) #!
        return "".join(self._code_table[s] for s in indices)
    

    # [7, 7, 7, 1, 0, 0] -> {7:3, 1:1, 0:2} -> derevo
    def _build_tree(self, indices: list[Any]) -> None:

        freq = Counter(indices)

        if len(freq) == 1:
            # [7, 7, 7] -> freq = {7: 3} -> sym = 7
            sym = next(iter(freq))
            self._tree = ("leaf", sym)
            self._code_table = {sym: "0"}
            return

        # Мин-куча: (частота, счетчик, узел-кортеж).
        #  Счетчик нужен как тай-брейкер при равных частотах.
        counter = 0
        heap: list[tuple] = []

        for sym, f in freq.items():
            heapq.heappush(heap,
                           (f, counter, ("leaf", sym)))
            counter += 1

        # Строим дерево Хафмана
        while len(heap) > 1:
            f1, _, sym1 = heapq.heappop(heap)
            f2, _, sym2 = heapq.heappop(heap)
            parent = ("internal", sym1, sym2)
            # Складывая частотности – идем к корню.
            #  Чем ближе к корню – тем выше частотность.
            #   Потом, вызвав _traverse(), мы обойдем дереро
            #    от корня до листьев: сначала коды 
            #     будут маленькие, а у листьев – большие.
            heapq.heappush(heap,
                           (f1 + f2, counter, parent))
            counter += 1

        # В конце в куче останется единственный элемент:
        #  тот, в котором самая большая частотность.
        #   Запишем его (кортеж) как корень дерева.
        self._tree = heapq.heappop(heap)[2]

        self._traverse(self._tree, "") #!


    # Рекурсивно обойти дерево
    def _traverse(self, node: tuple, prefix: str) -> None:
        if node[0] == "leaf":
            self._code_table[node[1]] = prefix or "0"
        # node[0] == "internal"
        else:
            self._traverse(node[1], prefix + "0") #!
            self._traverse(node[2], prefix + "1") #!


    # Используя дерево, сопоставить строке бит коды.
    #  Вернуть список индексов.
    def decode(self, bits: str) -> list[Any]:

        if self._tree is None:
            raise ValueError("Call \"encode\" first")

        # Частный случай: один уникальный символ.
        #  encode записывает "0" за каждое вхождение.
        if self._tree[0] == "leaf":
            return [self._tree[1]] * len(bits)

        result = []
        node   = self._tree

        for bit in bits:
            node = node[1] if bit == "0" else node[2]
            if node[0] == "leaf":
                result.append(node[1])
                node = self._tree
        return result


class LossyCompression:

    def __init__(self) -> None:

        self._huffman = HuffmanCoding() #!
        self._centers:  NDArrayFloat | None = None
        self._K:        int = 128

    # time_series -> indices -> _huffman.encode()
    def compress(self, time_series: NDArrayFloat) -> str:
        min = float(np.min(time_series))
        max = float(np.max(time_series))
        bounds = np.linspace(min, max, self._K + 1)
        self._centers = (bounds[ :-1] + bounds[1: ]) / 2.0
        # Каким отрезкам принадлежат исходные числа
        #  [ 0 9 21 2 9 ... ]
        indices: list[int] = \
            np.digitize( time_series, bounds[1:-1] ).tolist()
        return self._huffman.encode(indices) #!

    def decompress(self, bits: str) -> NDArrayFloat:

        # Берем строку бит, получаем массив индексов.
        indices = self._huffman.decode(bits) #!
        # Возвращаем усредненные значения по индексам.
        return    self._centers[np.array(indices, dtype=int)]


if __name__ == "__main__":
    
    ts                = np.loadtxt("practicum_5/homework/ts_homework_practicum_5.txt")
    compressor        = LossyCompression() #!
    
    bits              = compressor.compress(ts) #!
    ts_decompr        = compressor.decompress(bits) #!

    compression_ratio = (len(ts) * 32) / len(bits)
    compression_loss  = np.sqrt(np.mean((ts - ts_decompr)**2))

    print(f"Compression ratio:       {compression_ratio:.2f}")
    print(f"Compression loss (RMSE): {compression_loss}")

