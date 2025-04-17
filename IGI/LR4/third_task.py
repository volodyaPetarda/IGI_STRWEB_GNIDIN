import math
from utils import input_float
import statistics
import matplotlib.pyplot as plt

def my_sin(x):
    """
    Calculate sin(x) using Taylor series expansion.
    """
    x %= (2 * math.pi)
    term, result, n = x, x, 1
    while True:
        term *= -x * x / ((2 * n) * (2 * n + 1))
        result += term
        yield result
        n += 1


if __name__ == "__main__":
    x = input_float("Введите x: ")
    n = 500
    gen = my_sin(x)
    series = [next(gen) for _ in range(n)]

    mean = statistics.mean(series)
    median = statistics.median(series)
    mode = statistics.mode(series)
    variance = statistics.variance(series)
    stdev = statistics.stdev(series)

    print(f"Mean: {mean}")
    print(f"Median: {median}")
    print(f"Mode: {mode}")
    print(f"Variance: {variance}")
    print(f"Standard Deviation: {stdev}")

    real_sin = math.sin(x)

    plt.plot(range(n), series, label="Taylor Series", color="blue")
    plt.plot(range(n), [real_sin] * n, label="Math.sin", color="red")
    plt.xlabel("n")
    plt.ylabel("Value")
    plt.title("Taylor Series vs Math.sin")
    plt.legend()
    plt.savefig("data/taylor_vs_math_sin.png")
    plt.show()