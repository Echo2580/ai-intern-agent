import asyncio
import time

import httpx
import requests

url = "https://httpbin.org/delay/1"

total_start = time.perf_counter()

for _ in range(3):
    start = time.perf_counter()        # 拿高精度时间戳（秒，浮点）
    resp = requests.get(url)           # 同步发 GET，线程卡到服务器回才往下走
    cost = time.perf_counter() - start
    print(f"单次: {cost:.2f}s | 状态码 {resp.status_code}") # 结束 - 开始 = 这次请求耗时

total = time.perf_counter() - total_start


print(f"总耗时: {total:.2f}s | 平均耗时: {total/3:.2f}s")


# 定义一个协程函数：发一次异步 GET
async def fetch_one(client, i):
    start = time.perf_counter()
    resp = await client.get(url)          # await：停在这等网络回，控制权交出
    cost = time.perf_counter() - start
    print(f"异步 #{i}: {cost:.2f}s | 状态码 {resp.status_code}")

async def main():
    total_start = time.perf_counter()
    async with httpx.AsyncClient() as client:   # 异步上下文管理器
        # 同时发起 3 个请求，gather 收集所有结果
        tasks = [fetch_one(client, i) for i in range(3)]
        await asyncio.gather(*tasks)
    total = time.perf_counter() - total_start
    print(f"总耗时(异步): {total:.2f}s")

if __name__ == "__main__":
    asyncio.run(main())                          # 启动事件循环