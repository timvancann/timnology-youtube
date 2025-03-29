from typing import Callable

type Number = int | float
type Fun = Callable[[Number, Number], Number]


def multiply(a: Number, b: Number) -> Number:
    return a * b


def add(a: Number, b: Number) -> Number:
    return a + b


def apply(func: Fun, a: Number, b: Number) -> Number:
    return func(a, b)


print("add", apply(add, 2, 3))
print("multiply", apply(multiply, 2, 3))

op = multiply
print(op)
print("op", op(2, 3))


def choose_function_to_apply(name: str) -> Fun:
    if name == "add":
        return add
    return multiply


choice = choose_function_to_apply("add")
print(choice)
print(choice(2, 3))

result = choose_function_to_apply("add")(2, 7)
print(result)
