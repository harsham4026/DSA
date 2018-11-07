import math
import numbers


def standard_deviation(arr):
    mean = 0
    n = len(arr)
    for i in arr:
        if i is not None and isinstance(i, numbers.Number):
            mean += i
    mean = mean / n

    variance = 0

    for i in arr:
        if i is not None and isinstance(i, numbers.Number):
            variance += ((i - mean) * (i - mean))
    variance = variance / n

    print(variance)

    return math.sqrt(variance)


if __name__ == '__main__':
    arr = [1, 2, 3, 4, 5, 6, -80, None, 90.0, 0.0009]
    print(standard_deviation(arr))
