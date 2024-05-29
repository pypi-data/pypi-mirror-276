def add_one(n: int) -> int:
    return n + 1

def add_two(n: int) -> int:
    return add_one(add_one(n))

def add(x: int, y: int) -> int:
    sum = x
    for _ in range(y):
        sum = add_one(x)

    return sum
