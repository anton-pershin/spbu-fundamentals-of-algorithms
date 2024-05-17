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
        if not self.root:
            return []
        full_tree = []
        current_level = [self.root]
        inversed_drive = False
        while current_level:
            next_level = []
            current_values = []

            for node in current_level:
                current_values.append(node.key)
                if node.left:
                    next_level.append(node.left)
                if node.right:
                    next_level.append(node.right)

            if inversed_drive:
                current_values.reverse()

            full_tree.append(current_values)
            inversed_drive = not inversed_drive
            current_level = next_level

        return full_tree


def build_tree(list_view: list[Any]) -> BinaryTree:
    bt = BinaryTree()
    if not list_view:
        return bt
    bt.root = Node(list_view[0])
    inwork = [bt.root]

    i = 1
    while inwork and i < len(list_view):
        current = inwork.pop(0)
        if list_view[i] is not None:
            current.left = Node(list_view[i])
            inwork.append(current.left)
        i += 1
        if list_view[i] is not None:
            current.right = Node(list_view[i])
            inwork.append(current.right)
        i += 1

    return bt


if __name__ == "__main__":
    # Let's solve Binary Tree Zigzag Level Order Traversal problem from leetcode.com:
    # https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/
    # First, implement build_tree() to read a tree from a list format to our class
    # Second, implement BinaryTree.zigzag_traversal() returning the list required by the task
    # Avoid recursive traversal!

    with open(
        os.path.join(
            "binary_tree_zigzag_level_order_traversal_cases.yaml",
        ),
        "r",
    ) as f:
        cases = yaml.safe_load(f)

    for i, c in enumerate(cases):
        bt = build_tree(c["input"])
        zz_traversal = bt.zigzag_level_order_traversal()
        print(f"Case #{i + 1}: {zz_traversal == c['output']}")
