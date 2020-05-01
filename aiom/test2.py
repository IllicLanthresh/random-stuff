from timeit import default_timer as timer
import asyncio
import aiomultiprocess


aiomultiprocess.set_start_method('spawn')


def remove_if_prime(num, number_list):
    for div in range(2, num):
        if not num % div:
            number_list.remove(num)
            break


def stress_prime(number_list):
    start = timer()
    for num in number_list.copy():
        remove_if_prime(num, number_list)
    end = timer()
    print(end - start)
    return number_list


async def async_stress_prime(number_list):
    start = timer()
    tasks = [asyncio.coroutine(remove_if_prime)(num, number_list) for num in number_list.copy()]
    await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)
    end = timer()
    print(end - start)
    return number_list


# def chunk(l, n):
#     pass

# def pool_stress_prime(r, pool_count):
#
#     for _ in range(pool_count):
#         pools = []
#         async with aiomultiprocess.Pool() as pool:
#             print(await pool.map(get, urls))


BIG_NUMBER = 10000
POOL_COUNT = 4

print(*stress_prime(list(range(2, BIG_NUMBER + 1))), sep=', ')
print(*asyncio.run(async_stress_prime(list(range(2, BIG_NUMBER + 1)))), sep=', ')
# print(*pool_stress_prime(BIG_NUMBER, POOL_COUNT), sep=', ')
