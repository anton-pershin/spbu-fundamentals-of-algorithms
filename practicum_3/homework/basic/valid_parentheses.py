from typing import Any

import yaml
import numpy as np
from numpy.typing import NDArray

#from ...src.common import ProblemCase


class Stack:
    """LIFO queue"""

    def __init__(self, max_n: int, dtype: Any) -> None:
        self._array: NDArray = np.zeros((max_n,), dtype=dtype)  # internal array
        self._top_i: int = -1  # index of the most recently inserted element

    def empty(self) -> bool:
        return self._top_i == -1


    def push(self, x: Any) -> None:
        """Complexity: O(1)"""
        if len(self._array) == (self._top_i + 1):
           raise StackOverflowException("jdssksk")
        
        self._top_i += 1
        self._array[self._top_i] = x
        

    def pop(self) -> Any:
        """Complexity: O(1)"""
        if not self.empty():
            last_symbol = self._array[self._top_i]
            self._top_i -= 1
            return last_symbol
        else:
            raise StackUnderflowException('В последовательности недостаточно открывающихся скобок')
       

class StackUnderflowException(BaseException):
    '''В последовательности недостаточно открывающих скобок'''



class StackOverflowException(BaseException):
    '''В последовательности недостаточно закрывающих скобок'''
Ш

def get_starting_symbol(sym: str) -> str:
    if sym== ")":
        return "("
    elif sym == "]":
        return "["
    elif sym == "}":
        return "{"
    else:
        raise ValueError(f'Unknown parenthesis: "{sym}"')


def are_parentheses_valid(s: str) -> bool:
    st = Stack(len(s), dtype =str)
    for i in s:
        if i in "([{":
            st.push(i)
        else:
            if st.empty():
                return False
            
            last = st.pop()
            if get_starting_symbol(i) != last:
                return False
            
    if not st.empty():
        return False
    return True

if __name__ == "__main__":
    # Let's solve Valid Parentheses problem from leetcode.com:
    # https://leetcode.com/problems/valid-parentheses/
    cases = []
    with open("practicum_3/homework/basic/valid_parentheses_cases.yaml", "r") as f:
        cases = yaml.safe_load(f)
    for c in cases:
        print(c)
        res = are_parentheses_valid(c["input"])

        print(f"Input: {c['input']}. Output: {res}. Expected output: {c['output']}")
