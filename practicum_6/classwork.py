def square (x: int) -> int:
    return x*x
square

type(square)

square.__name__

def apply(xs: list[int], func) -> list [int]:
    return [func(x) for x in xs]
a = [1, 2, 3]
apply (a, square)

from typing import Callable
def apply(xs: list[int], func: Callable[[int], int]) -> list [int]:
    return [func(x) for x in xs]

class MegaSquare:
    def __call__(self, x:int ) -> int:
        return x*x
ms = MegaSquare()
ms(10)

class megasquare:
    def __init__(self, a, b) -> None:
        self.a = a
        self.b = b
    def __call__(self, x:int) -> int:
        return (self.a + x) * (self.b + x)
ms = megasquare(a=10, b=5)
ms(3)

a = [3, 5, 4, 2, 1]
sorted(a)

b = [{"x": 5, "y": 3}, {"x": 2, "y": 0}, {"x": 4, "y": -999}]
b

from operator import itemgetter
sorted(b, key = itemgetter("x"))

def custom_itemgetter(elem):
    return elem["x"]
sorted(b, key = custom_itemgetter)

def custom_itemgetter(key:str):
    def _itemgetter(elem):
        return elem[key]
    return _itemgetter
custom_itemgetter("x")
sorted(b, key=custom_itemgetter("x"))

a
map(square, a)
for elem in map(square, a):
    print(elem)

from functools import reduce
from operator import add
def custom_add(x, y):
    return x + y
reduce(add, map(square, a), 0)

c = [[1,2,3], [4,5,6], [7,8,9]]
reduce(add, c, [])

d = [-3, -4, 5, 1, 2]
def positive(x):
    return x > 0
filter(positive, d)
for element in filter(positive, d):
    print(element)

def foo(x: int, flag: bool) -> int:
    if flag: 
        return x
    else: 
        return -x
from functools import partial
foo_with_flag_true = partial(foo, flag=True)
foo_with_flag_false = partial(foo, flag=False)
foo_with_flag_true(10)
foo_with_flag_false(10)
foo_with_flag_true([1, 2])