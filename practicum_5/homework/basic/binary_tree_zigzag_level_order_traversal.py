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


class BinaryTree:
    def __init__(self) -> None:
        self.root: Node = None

    def empty(self) -> bool:
        return self.root is None

    def zigzag_level_order_traversal(self) -> list[Any]:
        if self.root is None:
            return []

        result = []
        current_level = [self.root]
        level_num = 0

        while current_level:
            next_level = []
            values = []

            for node in current_level:
                values.append(node.key)

                if node.left:
                    next_level.append(node.left)
                if node.right:
                    next_level.append(node.right)

            if level_num % 2 == 0:
                result.extend(values)
            else:
                result.extend(values[::-1])

            current_level = next_level
            level_num += 1

        return result
    
def build_tree(list_view: list[Any]) -> BinaryTree:
    bt = BinaryTree()

    if not list_view:
        return bt

    nodes = [None if val is None else Node(val) for val in list_view]
    bt.root = nodes[0]

    for i, node in enumerate(nodes):
        if node is None:
            continue

        left_child_index = 2 * i + 1
        right_child_index = 2 * i + 2

        if left_child_index < len(nodes):
            node.left = nodes[left_child_index]

        if right_child_index < len(nodes):
            node.right = nodes[right_child_index]

    return bt

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
        bt = build_tree(c["input"])
        zz_traversal = bt.zigzag_level_order_traversal()
        print(f"Case #{i + 1}: {zz_traversal == c['output']}")
