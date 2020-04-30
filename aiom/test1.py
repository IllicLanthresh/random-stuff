from math import pi, tan, atan
from random import random


BIG_NUMBER = pow(10, 5)

def stress_tan(r):
    x = 2 * pi * random()
    for _ in range(r+1):
        x = atan(tan(x))
    return x


def stress_prime(r):
    primes = []
    for num in range(2, r+1):
        primes.append(num)
        for div in range(2, num):
            if not num%div:
                primes.remove(num)
                break
    return primes


def stress_factorial(x):
    result = 1
    for num in range(1, x + 1):
        result *= num
    return result

for i in range(1, 10, 2):
    print(f'pow {i}:')
    print('\t%timeit:')
    print('\t\tprime:\t\t', end='')
    %timeit stress_prime(pow(10, i))
    print('\t\tfactorial:\t', end='')
    %timeit stress_factorial(pow(10, i))
    print('\t\ttan:\t\t', end='')
    %timeit stress_tan(pow(10, i))
    print('\n')
    print('\t%time:')
    print('\t\tprime:\t\t', end='')
    %time stress_prime(pow(10, i))
    print('\t\tfactorial:\t', end='')
    %time stress_factorial(pow(10, i))
    print('\t\ttan:\t\t', end='')
    %time stress_tan(pow(10, i))
    print('\n\n')

