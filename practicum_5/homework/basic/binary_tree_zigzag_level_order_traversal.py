from __future__ import annotations
from dataclasses import dataclass
from typing import Any
import os

import yaml


@dataclass
class Node:
    key: Any
    data: Any = None
    left: Node = None
    right: Node = None

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


class BinaryTree:
    def __init__(self) -> None:
        self.root: Node = None

    def empty(self) -> bool:
        return self.root is None

    def build_tree(self, values: list[int]) -> None:
        if not values:
            return
        self.root = Node(values[0])
        queue = [self.root]
        i = 1
        while queue:
            node = queue.pop(0)
            if i < len(values):
                if values[i] is not None:
                    node.left = Node(values[i])
                    queue.append(node.left)
            i += 1
            if i < len(values):
                if values[i] is not None:
                    node.right = Node(values[i])
                    queue.append(node.right)
            i += 1

    def zigzag_level_order_traversal(self) -> list[Any]:
        if self.empty():
            return []

        result, level = [], 0
        queue = [self.root]

        while queue:
            level_nodes = []
            level_size = len(queue)

            if level % 2 == 0:
                for _ in range(level_size):
                    node = queue.pop(0)

                    level_nodes.append(node.val)
                    if node.left:
                        queue.append(node.left)
                    if node.right:
                        queue.append(node.right)

            else:
                for _ in range(level_size):
                    node = queue.pop()
                    level_nodes.append(node.val)
                    if node.right:
                        queue.insert(0, node.right)
                    if node.left:
                        queue.insert(0, node.left)

            result.append(level_nodes)
            level += 1

        return result


if __name__ == "__main__":
    # Let's solve Binary Tree Zigzag Level Order Traversal problem from leetcode.com:
    # https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/
    # First, implement build_tree() to read a tree from a list format to our class
    # Second, implement BinaryTree.zigzag_traversal() returning the list required by the task
    # Avoid recursive traversal!

    with open(
            os.path.join(
                "practicum_5",
                "homework",
                "basic",
                "binary_tree_zigzag_level_order_traversal_cases.yaml",
            ),
            "r",
    ) as f:
        cases = yaml.safe_load(f)

    for i, c in enumerate(cases):
        bt = BinaryTree()
        bt.build_tree(c["input"])

        zz_traversal = bt.zigzag_level_order_traversal()
        print(f"Case #{i + 1}: {zz_traversal == c['output']}")