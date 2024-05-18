from typing import Any

import yaml
import numpy as np
from numpy.typing import NDArray

from src.common import ProblemCase


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
            print("Error")
            return
        self._top_i += 1
        self._array[self._top_i] = x

    def pop(self) -> Any:
        """Complexity: O(1)"""
        if self.empty():
            print("Error")
            return None
        x = self._array[self._top_i]
        # self._array[self._top_i] = 0
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
    st = Stack(len(s), str)
    for i in range(len(s)):
        if s[i] == "(" or s[i] == "[" or s[i] == "{":
            st.push(s[i])
        elif s[i] == ")" or s[i] == "]" or s[i] == "}":
            if st._array[st._top_i] == get_starting_symbol(s[i]):
                st.pop()
            else:
                return False
    return st.empty()


if __name__ == "__main__":
    # Let's solve Valid Parentheses problem from leetcode.com:
    # https://leetcode.com/problems/valid-parentheses/
    cases = []
    with open("D:/spbu-fundamentals-of-algorithms/practicum_3/homework/basic/valid_parentheses_cases.yaml", "r") as f:
        cases = yaml.safe_load(f)
    for c in cases:
        res = are_parentheses_valid(c["input"])
        print(f"Input: {c['input']}. Output: {res}. Expected output: {c['output']}")
