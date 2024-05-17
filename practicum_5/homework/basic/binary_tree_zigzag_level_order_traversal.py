from __future__ import annotations
from dataclasses import dataclass
from typing import Any
import os

import yaml


@dataclass
class Node:
    # key: Any
    data: Any = None
    left: Node = None
    right: Node = None

class BinaryTree:
    def __init__(self) -> None:
        self.root: Node = None
        self.nodes: list = []

    def empty(self) -> bool:
        return self.root is None

    def zigzag_level_order_traversal(self) -> list[Any]:
        if self.empty():
            return []

        result = []
        current_level = [self.root]
        orientation = 1

        while current_level:
            next_level = []
            current_values = []
            for node in current_level:
                if node.data != None:
                    current_values.append(node.data)
                if node.left:
                    next_level.append(node.left)
                if node.right:
                    next_level.append(node.right)
            if orientation == -1:
                current_values = current_values[::-1]
            result.append(current_values)
            current_level = next_level
            orientation *= -1

        return result
    

def build_Node(bt: BinaryTree, list_view: list[Any], index: int) -> Node:
    node = Node()
    if index<len(list_view):
        node.data = list_view[index]
        if (index*2+1) < len(list_view):
            node.left = build_Node(bt, list_view, index*2+1)
            node.right = build_Node(bt, list_view, index*2+2)
        bt.nodes.append(node)
    return node


def build_tree(list_view: list[Any]) -> BinaryTree:
    bt = BinaryTree()
    build_Node(bt, list_view, 0)
    if len(bt.nodes) > 0:
        bt.root = bt.nodes[len(bt.nodes)-1]
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
        # print(bt.nodes)
        # print(bt.root)
        zz_traversal = bt.zigzag_level_order_traversal()
        print(f"Case #{i + 1}: {zz_traversal == c['output']}")
