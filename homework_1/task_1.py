from math import sqrt, floor

phi = (1 + sqrt(5)) / 2

def nth_fib(n):
    """
    Returns the nth fibonacci number.
    :param n: int
    :return: int
    """
    return floor((phi ** n) / sqrt(5) + 0.5)

print(nth_fib(7))