from typing import Any

import yaml
import numpy as np
from numpy.typing import NDArray

from src.common import ProblemCase


class Stack:

    def __init__(self, max_n: int, dtype: Any) -> None:
        self._array: NDArray = np.zeros((max_n,), dtype=dtype)  
        self._top_i: int = -1  

    def empty(self) -> bool:
        return self._top_i == -1

    def push(self, x: Any) -> None:
        if self._top_i == len(self._array) - 1:
            raise StackOverflowException("Stack is full")
        self._top_i += 1
        self._array[self._top_i] = x

    def pop(self) -> Any:
        if self.empty():
            raise StackUnderflowException("Stack is empty")
        x = self._array[self._top_i]
        self._top_i -= 1
        return x


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
    stack = Stack(len(s), str)
    for char in s:
        if char in "([{":
            stack.push(char)
        elif char in ")]}":
            if stack.empty() or stack.pop() != get_starting_symbol(char):
                return False
    return stack.empty()


if __name__ == "__main__":

    cases = []
    with open(valid_parentheses_cases.yaml, "r") as f:
        cases = yaml.safe_load(f)
    for c in cases:
        res = are_parentheses_valid(c["input"])
        print(f"Input: {c['input']}. Output: {res}. Expected output: {c['output']}")
