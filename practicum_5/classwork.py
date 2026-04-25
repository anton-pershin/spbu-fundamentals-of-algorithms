a = {"x": 0, "y": 10}
a

a["x"]

a["y"]

from typing import TypedDict
class A(TypedDict):
    x: int
    y: int
a = A(x = 0, y = 10)
a

a["x"]

a["y"]

mypy, pylint
a["x"] = 0
a["x"] = "qwer"

from dataclasses import dataclass
@dataclass
class A:
    x: int
    y: int

class A: 
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

a = A(x = 0, y = 10)
a.x

a.y

a.z

a.x = "qwer"
@dataclass(frozen=True)
class A:
    x: int
    y: int
a = A(x= 0, y = 10)
a.x

a.y

a.x = 0
#err

hash(a)

b = A(x = 10, y = 10)
a

b

a == b
#false

@dataclass
class A:
    x: int
    y: int
    def __post_init__(self) -> None:
        if self.y < 0:
            raise ValueError(f"y must be > 0")
a = A(x = 0, y = 10)
a = A(x = 0, x = -10)

class A:
    def __init__(self, x:int, y: int) -> None:
        self._x = x
        self._y = y
        @property
        def x(self) -> int:
            print(f"smone touched x")
            return self._x
        @x.setter
        def x(self, value: int) -> None:
            print(f"someone assigned {value} to x")
            if value < 0:
                raise ValueError("must be > 0")
            self._x = value

a = A(x = 0, y = 10)
a._x

a._y

a.x

a.y

5 + 2. / (a.x + 1)

a.x = 100

a.x
        
a.x = -10

from pydantic import BaseModel
class A(BaseModel):
    x: int
    y: int

A.model_validate({"x": 0, "y" : 10})

A.model_validate({"x": 0, "y" : "qwer"})
#err

from pydantic import NonNegativeInt
class A(BaseModel):
    x: int
    y: NonNegativeInt
a = A.model_validate({"x": 0, "y" : -10})
#err