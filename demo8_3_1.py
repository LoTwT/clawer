# 异步爬虫
# 协程基础

import time
import asyncio
from aiohttp import ClientSession


def hello_sync(count):
    print(f'{count}: 开始时间戳：{time.time()}')
    time.sleep(1)
    print(f'{count}: 结束时间戳：{time.time()}')


def run_sync():
    for i in range(5):
        hello_sync(i)


async def hello_async(count):
    print(f'{count}: Hello Maishu! 开始时间戳：{time.time()}')
    await asyncio.sleep(1)
    print(f'{count}: Hello Maishu! 结束时间戳：{time.time()}')


async def run_async():
    tasks = []
    for i in range(5):
        task = asyncio.create_task(hello_async(i))
        tasks.append(task)
    for task in tasks:
        await task


async def run_aiohttp(url):
    async with ClientSession() as session:
        async with session.get(url) as response:
            print(response.status)


async def run_aiohttp_parallel():
    url = "http://www.baidu.com"
    urls = [url, url, url, url, url]

    tasks = []
    for u in urls:
        task = asyncio.create_task(run_aiohttp(u))
        tasks.append(task)

    for task in tasks:
        await task


if __name__ == '__main__':
    # run_sync()  # 同步
    # asyncio.run(run_async())  # 异步
    # asyncio.run(run_aiohttp("http://www.baidu.com"))  # aiohttp
    asyncio.run(run_aiohttp_parallel())  # 并行 aiohttp
