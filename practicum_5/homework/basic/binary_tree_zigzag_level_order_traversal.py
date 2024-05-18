from __future__ import annotations
from dataclasses import dataclass
from collections import deque
from typing import Any
import os

import yaml


@dataclass
class Node:
    key: Any
    data: Any = None
    left: Node = None
    right: Node = None


class BinaryTree:
    def __init__(self) -> None:
        self.root: Node = None

    def empty(self) -> bool:
        return self.root is None

    def zigzag_level_order_traversal(self) -> list[Any]:
        if not self.root: #проверка непустое ли дерево
            return []
        result = []
        level = []
        s1 = [self.root]
        s2 = []
        while s1 or s2:
            while s1:
                node = s1.pop()
                level.append(node.key)
                if node.left:
                    s2.append(node.left)
                if node.right:
                    s2.append(node.right)
                #в s2 поместили [9,20]
            if level:
                result.append(level)
            level = []

            while s2:
                node = s2.pop() # получаем [20,9]
                level.append(node.key)
                if node.right:
                    s1.append(node.right)
                if node.left:
                    s1.append(node.left)
            if level:
                result.append(level) #записываем в result [20,9]
            level =[]
        return result


def build_tree(list_view: list[Any]) -> BinaryTree:
    bt = BinaryTree()

    if not list_view:
        return bt

    # Создаем корень дерева из первого элемента списка
    bt.root = Node(key=list_view[0])
    queue = deque([bt.root])

    # Индекс для перемещения по списку
    index = 1

    # Пока у нас есть узлы в очереди и элементы в списке
    while queue and index < len(list_view):
        # Извлекаем текущий узел из очереди
        current_node = queue.popleft()

        # Создаем левого потомка текущего узла
        if list_view[index] is not None:
            current_node.left = Node(key=list_view[index])
            queue.append(current_node.left)

        # Переходим к следующему элементу списка
        index += 1

        # Создаем правого потомка текущего узла
        if index < len(list_view) and list_view[index] is not None:
            current_node.right = Node(key=list_view[index])
            queue.append(current_node.right)

        # Переходим к следующему элементу списка
        index += 1

    return bt


if __name__ == "__main__":
    # Let's solve Binary Tree Zigzag Level Order Traversal problem from leetcode.com:
    # https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/
    # First, implement build_tree() to read a tree from a list format to our class
    # Second, implement BinaryTree.zigzag_traversal() returning the list required by the task
    # Avoid recursive traversal!

    with open("practicum_5\homework\basic\binary_tree_zigzag_level_order_traversal_cases.yaml", "r") as f:
        cases = yaml.safe_load(f)

    for i, c in enumerate(cases):
        bt = build_tree(c["input"])
        zz_traversal = bt.zigzag_level_order_traversal()
        print(f"Case #{i + 1}: {zz_traversal == c['output']}")
