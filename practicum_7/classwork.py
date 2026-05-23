def apply(x: list[int], func) -> list[int]:
    return [func(x_) for x_ in x]

def square(x: int) -> int:
    return x * x

a = [1, 2, 3]
apply(a, func=square)

apply(a, func= lambda x: x * x)

def outer(x: int):
    def inner(y: int) -> int:
        return x * y
    return inner

outer(3)
outer(3)(5)
func = outer(3)
func(2)
func(6)

def make_counter():
    count = 0
    def inc() -> int:
        print(count)
    return inc

make_counter()
make_counter()()

def make_counter():
    count = 0
    def inc() -> int:
        count += 1
        return count
    return inc

func = make_counter()
func() #err

def make_counter():
    count = 0
    def inc() -> int:
        nonlocal count
        count += 1
        return count
    return inc

func = make_counter()
func()
func()

def count_calls(func):
    calls = 0
    def wrapper(*args, **kwargs):
        nonlocal calls
        calls += 1
        print(f"Function {func.__name__} has been called {calls} times")
        return func(*args, **kwargs)
    return wrapper
func = count_calls(square)
func(5)
func(10)

@count_calls
def square(x: int) -> int:
    return x * x    
square(5)
square(10)

def repeat(times: int):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = ""
            for _ in range(times):
                result += func(*args, **kwargs)
            return result
        return wrapper
    return decorator
@repeat(times=3)
def say_hello():
    return f"Hello! "
say_hello()

@count_calls
@repeat(times=3)
def say_hello():
    return f"Hello! "
say_hello()

def foo(*args, **kwargs):
    print(f"args: {args}, kwargs: {kwargs}")
foo(1, 2, 3, a=4, b=5)