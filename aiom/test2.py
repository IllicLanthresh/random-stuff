from math import ceil
import asyncio
import aiomultiprocess

from timeit import default_timer as timer


class Test:
    BIG_NUMBER = 100000

    def __init__(self):
        self.number_list = list(range(2, Test.BIG_NUMBER + 1))


class SyncTest(Test):
    def remove_if_prime(self, num):
        for div in range(2, num):
            if not num % div:
                self.number_list.remove(num)
                break

    def test(self):
        start = timer()
        for num in self.number_list.copy():
            self.remove_if_prime(num)
        end = timer()
        print(end - start)
        return self.number_list


class AsyncTest(Test):
    def __init__(self):
        super().__init__()
        self.loop = asyncio.get_event_loop()

    async def remove_if_prime(self, num):
        for div in range(2, num):
            if not num % div:
                self.number_list.remove(num)
                break

    async def coro(self):
        start = timer()
        tasks = [self.remove_if_prime(num) for num in self.number_list.copy()]
        await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)
        end = timer()
        print(end - start)
        return self.number_list

    def test(self):
        return self.loop.run_until_complete(self.coro())


class PoolTest(Test):
    POOL_COUNT = 4
    METHOD = 'spawn'

    def __init__(self):
        super().__init__()
        aiomultiprocess.set_start_method(PoolTest.METHOD)
        self.chunks = self.make_chunks()

    def make_chunks(self):
        chunks = []
        max_chunk_size = ceil(len(self.number_list) / PoolTest.POOL_COUNT)
        for i in range(PoolTest.POOL_COUNT):
            chunk = self.number_list[i * max_chunk_size:(i + 1) * max_chunk_size]
            if chunk:
                self.chunks.append(chunk)
        return chunks

    def remove_if_prime(self, num):
        for div in range(2, num):
            if not num % div:
                self.number_list.remove(num)
                break

    def pool_stress_prime(self):

        for _ in range(PoolTest.POOL_COUNT):
            pools = []
            async with aiomultiprocess.Pool() as pool:
                print(await pool.map(get, urls))

    def test(self):
        pass


print(*SyncTest().test(), sep=', ')
print(*AsyncTest().test(), sep=', ')
print(*PoolTest().test(), sep=', ')
