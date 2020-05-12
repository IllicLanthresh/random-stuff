from math import ceil
import orjson
import asyncio
import aiomultiprocess

from timeit import default_timer as timer


class Test:
    PAYLOADS = {
        str: {
            "empty": "",
            "small": "SMALLPAYLOAD____" * 10,
            "medium": "MEDIUMPAYLOAD___" * 100,
            "big": "BIGPAYLOAD______" * 1000,
            "huge": "HUGEPAYLOAD_____" * 10000,
            "killer": "HUGEPAYLOAD_____" * 10000000,
        },
        dict: {
            "empty": {},

            "small": {chr(x): chr(x) * 10 \
                      for x in range(ord("a"), ord("a") + 10)},

            "medium": {chr(x): chr(x) * 100 \
                       for x in range(1, 100)},

            "big": {chr(x): chr(x) * 1000 \
                    for x in range(1, 1000)},

            "huge": {chr(x): chr(x) * 10000 \
                     for x in range(1, 10000)},

            # "killer": { chr(x): chr(x) * 10000000 \
            #     for x in range(1, 10000000 ) },
        }
    }

    def test(self):
        """ Override this method to implement the test start action"""
        raise NotImplementedError


class SingleCoreTest(Test):
    def __init__(self):
        self.number_list = []

    @staticmethod
    def is_prime(num):
        for div in range(2, num):
            if num % div == 0:
                return False
        return True

    def test(self):
        start = timer()
        self.number_list = [num for num in range(2, self.BIG_NUMBER + 1) if self.is_prime(num)]
        end = timer()
        print(end - start)
        return self.number_list


class AsyncioTest(Test):
    def __init__(self):
        self.number_list = list(range(2, Test.BIG_NUMBER + 1))
        self.loop = asyncio.get_event_loop()

    async def remove_if_not_prime(self, num):
        for div in range(2, num):
            if not num % div:
                self.number_list.remove(num)
                break

    async def coro(self):
        start = timer()
        tasks = [self.remove_if_not_prime(num) for num in self.number_list.copy()]
        await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)
        end = timer()
        print(end - start)
        return self.number_list

    def test(self):
        return self.loop.run_until_complete(self.coro())


class PoolTest(Test):
    QUEUE_COUNT = 6
    CHUNK_COUNT = 6
    METHOD = 'spawn'

    def __init__(self):
        self.number_list = list(range(2, Test.BIG_NUMBER + 1))
        self.loop = asyncio.get_event_loop()
        aiomultiprocess.set_start_method(PoolTest.METHOD)
        self.chunks = self.make_chunks()

    def make_chunks(self):
        chunks = []
        max_chunk_size = ceil(len(self.number_list) / self.CHUNK_COUNT)
        for i in range(self.CHUNK_COUNT):
            chunk = self.number_list[i * max_chunk_size:(i + 1) * max_chunk_size]
            if chunk:
                chunks.append(chunk)
        return chunks

    @staticmethod
    async def remove_not_primes(numlist):
        for num in list(numlist):
            for div in range(2, num):
                if not num % div:
                    numlist.remove(num)
                    break
        return numlist

    async def coro(self):
        start = timer()
        async with aiomultiprocess.Pool(queuecount=self.QUEUE_COUNT) as pool:
            cleaned_chunks = await pool.map(self.remove_not_primes, self.chunks)
        end = timer()
        print(end - start)
        return [num for chunk in cleaned_chunks for num in chunk]

    def test(self):
        return self.loop.run_until_complete(self.coro())


if __name__ == '__main__':
    print(*SingleCoreTest().test(), sep=', ')
    print(*AsyncioTest().test(), sep=', ')
    print(*PoolTest().test(), sep=', ')
