import asyncio
from math import ceil
from timeit import default_timer as timer

import aiomultiprocess
import orjson


class Test:
    PAYLOADS = {
        "small": {chr(x): chr(x) * 10 for x in range(ord("a"), ord("a") + 10)},

        "medium": {chr(x): chr(x) * 100 for x in range(1, 100)},

        "big": {chr(x): chr(x) * 1000 for x in range(1, 1000)},

        "huge": {chr(x): chr(x) * 10000 for x in range(1, 10000)},

        # "killer": {chr(x): chr(x) * 10000000 for x in range(1, 10000000)},
    }

    def __init__(self, dict_count, t):
        if t is None:
            t = 'big'
        self.list_of_dicts = [self.PAYLOADS[t] for _ in range(dict_count)]

    def test(self):
        """ Override this method to implement the test start action"""
        raise NotImplementedError


class SyncronousTest(Test):
    def __init__(self, dict_count, t: str = None):
        super().__init__(dict_count, t=t)

    @staticmethod
    def encode(data):
        return orjson.dumps(data)

    @staticmethod
    def decode(data):
        return orjson.loads(data)

    def test(self):
        result = []
        start = timer()
        for d in self.list_of_dicts:
            serialized = self.encode(d)
            result.append(self.decode(serialized))
        end = timer()
        print(end - start)
        return result


class AsyncioTest(Test):
    def __init__(self, dict_count, t: str = None):
        super().__init__(dict_count, t=t)
        self.loop = asyncio.get_event_loop()

    @staticmethod
    async def encode(data):
        return orjson.dumps(data)

    @staticmethod
    async def decode(data):
        return orjson.loads(data)

    async def coro(self):
        # This is not async but...
        result = []
        start = timer()
        for d in self.list_of_dicts:
            serialized = await self.encode(d)
            result.append(await self.decode(serialized))
        end = timer()
        print(end - start)
        return result

    def test(self):
        return self.loop.run_until_complete(self.coro())


class PoolTest(Test):
    def __init__(self,
                 dict_count,
                 t: str = None,
                 process_count: int = None,
                 queue_count: int = 6,
                 chunk_count: int = 6,
                 method: str = 'spawn'):
        super().__init__(dict_count, t)
        self.process_count = process_count
        self.queue_count = queue_count
        self.chunk_count = chunk_count
        self.method = method
        self.loop = asyncio.get_event_loop()
        aiomultiprocess.set_start_method(self.method)
        self.chunks = self.make_chunks()

    @staticmethod
    def encode(data):
        return orjson.dumps(data)

    @staticmethod
    def decode(data):
        return orjson.loads(data)

    @staticmethod
    async def chain(chunk):
        result = []
        for data in chunk:
            serialized = PoolTest.encode(data)
            result.append(PoolTest.decode(serialized))
        return result

    async def coro(self):
        # This is not async but...
        result = []
        start = timer()
        async with aiomultiprocess.Pool(processes=self.process_count, queuecount=self.queue_count) as pool:
            result = [d for c in await pool.map(self.chain, self.chunks) for d in c]
        end = timer()
        print(end - start)
        return result

    def make_chunks(self):
        chunks = []
        max_chunk_size = ceil(len(self.list_of_dicts) / self.chunk_count)
        for i in range(self.chunk_count):
            chunk = self.list_of_dicts[i * max_chunk_size:(i + 1) * max_chunk_size]
            if chunk:
                chunks.append(chunk)
        return chunks

    def test(self):
        return self.loop.run_until_complete(self.coro())


if __name__ == '__main__':
    SyncronousTest(100).test()
    AsyncioTest(100).test()
    PoolTest(100).test()

    # print(*AsyncioTest().test(), sep=', ')
    # print(*PoolTest().test(), sep=', ')
