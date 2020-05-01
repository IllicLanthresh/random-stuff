from timeit import default_timer as timer
import asyncio
import functools
import aiomultiprocess

from math import pi, tan, atan
from random import random

aiomultiprocess.set_start_method('spawn')


async def async_append_if_prime(num, primes):
    # print(num, end=', ')
    append = True
    for div in range(2, num):
        if not num % div:
            append = False
            break
    if append:
        primes.append(num)


async def async_stress_prime(r):
    start = timer()
    primes = []
    tasks = [asyncio.ensure_future(async_append_if_prime(num, primes)) for num in range(2, r + 1)]
    await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)
    end = timer()
    print(end - start)
    return primes


def stress_prime(r):
    start = timer()
    primes = []
    for num in range(2, r + 1):
        # print(num, end=', ')
        primes.append(num)
        for div in range(2, num):
            if not num % div:
                primes.remove(num)
                break
    end = timer()
    print(end - start)
    return primes


BIG_NUMBER = 100000
print(stress_prime(BIG_NUMBER))
print(asyncio.run(async_stress_prime(BIG_NUMBER)))

# for _ in range(BIG_NUMBER//100):
#     async with aiomultiprocess.Pool() as pool:
#         print(await pool.map(get, urls))
