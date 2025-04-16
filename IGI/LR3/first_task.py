import math
from utils import input_float

def my_sin(x, eps):
    """
    Calculate sin(x) using Taylor series expansion.
    """
    x %= (2 * math.pi)
    term, result, n = x, x, 1
    while abs(term) > eps and n < 500:
        term *= -x * x / ((2 * n) * (2 * n + 1))
        result += term
        n += 1

    return n, result

if __name__ == "__main__":
    x = input_float("Введите x: ")
    eps = input_float("Введите точность eps: ")

    n, my_result = my_sin(x, eps)
    math_result = math.sin(x)
    print(f"x = {x}, n = {n}, my_sin(x) = {my_result}, math_result = {math_result}, eps = {abs(math_result - my_result)}")

