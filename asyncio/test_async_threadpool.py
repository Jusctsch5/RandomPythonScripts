from concurrent.futures import ThreadPoolExecutor
import random
import time
import asyncio

# You would use weather_detail here
async def get_random(n0, n1):
    await asyncio.sleep(3.0)
    return random.randint(n0, n1)

def wrapper(coro):
    return asyncio.run(coro)

def main():
    print("Start", time.ctime())
    with ThreadPoolExecutor(max_workers=3) as executor:
        arglist = ((10, 20), (30, 40), (50, 60), (90, 100))
        coros = [get_random(n0, n1) for n0, n1 in arglist]
        for r in executor.map(wrapper, coros):
            print(r, time.ctime())

def run_one():
    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.submit()



main()