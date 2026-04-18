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
