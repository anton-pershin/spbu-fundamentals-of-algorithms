import numpy as np
from numpy import ndarray as NDArray
from typing import Any
import yaml


class Stack:
    """LIFO queue"""

    def __init__(self, max_n: int, dtype: Any) -> None:
        self._array: NDArray = np.zeros((max_n,), dtype=dtype)  # internal array
        self._top_i: int = -1  # index of the most recently inserted element

    def empty(self) -> bool:
        return self._top_i == -1

    def push(self, x: Any) -> None:
        """Complexity: O(1)"""
        if self._top_i == len(self._array) - 1:
            raise StackOverflowException("Stack overflow")
        self._top_i += 1
        self._array[self._top_i] = x

    def pop(self) -> Any:
        """Complexity: O(1)"""
        if self.empty():
            raise StackUnderflowException("Stack underflow")
        item = self._array[self._top_i]
        self._top_i -= 1
        return item


class StackUnderflowException(BaseException):
    pass


class StackOverflowException(BaseException):
    pass


def get_starting_symbol(sym: str) -> str:
    if sym == ")":
        return "("
    elif sym == "]":
        return "["
    elif sym == "}":
        return "{"
    else:
        raise ValueError(f'Unknown parenthesis: "{sym}"')


def are_parentheses_valid(s: str) -> bool:
    stack = Stack(len(s), dtype=str)
    for sym in s:
        if sym in "([{":
            stack.push(sym)
        elif sym in ")]}":
            if stack.empty():
                return False
            start_sym = get_starting_symbol(sym)
            if stack.pop() != start_sym:
                return False
    return stack.empty()


if __name__ == "__main__":
    cases = []
    with open("valid_parentheses_cases.yaml", "r") as f:
        cases = yaml.safe_load(f)
    for c in cases:
        res = are_parentheses_valid(c["input"])
        print(f"Input: {c['input']}. Output: {res}. Expected output: {c['output']}")
