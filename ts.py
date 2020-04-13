def f(x):
    return 2*x**2-12*x+7


def findMinWithTernarySearch(low, high):
    while True:
        if low == high - 1:
            return min(f(low), f(high))
        mid1 = low + (high-low)//3
        mid2 = high - (high-low)//3
        f1 = f(mid1)
        f2 = f(mid2)
        if f1 < f2:
            high = mid2 - 1
        elif f1 > f2:
            low = mid1 + 1


print(findMinWithTernarySearch(-257, 364))
