import time
import asyncio
import sys

async def some_func():
    LAST_CHECKED_TIME = time.time()
    while True:
        if time.time() - LAST_CHECKED_TIME >= 1:
            LAST_CHECKED_TIME = time.time()
            print("-", end="")
            sys.stdout.flush()
        await asyncio.sleep(0.5)

async def some_other_func():
    counter = 0
    LAST_CHECKED_TIME = time.time()
    while True:
        if time.time() - LAST_CHECKED_TIME >= 1:
            counter += 1
            LAST_CHECKED_TIME = time.time()
            print(counter, end="")
            sys.stdout.flush()
        await asyncio.sleep(0.5)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(some_func(), some_other_func()))