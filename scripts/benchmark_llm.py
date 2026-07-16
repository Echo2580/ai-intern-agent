import asyncio
import time

import httpx
import requests

JD = (
    "我们正在寻找一名高级 Python 后端工程师，加入我们的 AI 平台团队。"
    "岗位职责：1. 负责 LLM 应用后端服务的设计与开发，基于 FastAPI 构建高并发 API；"
    "2. 设计并实现 RAG 检索增强生成链路，对接向量数据库；"
    "3. 优化 Agent 工作流编排，提升系统吞吐与稳定性；"
    "4. 编写单元测试与接口文档，参与代码评审。"
    "任职要求：1. 本科及以上学历，计算机相关专业，3 年以上后端开发经验；"
    "2. 精通 Python，熟悉 FastAPI / Django / Flask 至少一种框架；"
    "3. 熟悉 PostgreSQL、Redis、向量数据库（如 Milvus / pgvector）；"
    "4. 有 LLM / RAG / Agent 实际项目落地经验者优先；"
    "5. 具备良好的英文文档阅读能力，能承受一定工作压力。"
)
BASE = "http://127.0.0.1:8000/api/v1/jd/analyze-basic-llm"

def run_sync(n=3):
    t0 = time.perf_counter()
    for i in range(n):
        r = requests.post(BASE, json={"jd_text": JD})
        print(f"sync #{i}: {r.status_code}")
    print(f"同步总耗时: {time.perf_counter() - t0:.2f}s")

async def one(client, i):
    r = await client.post(BASE, json={"jd_text": JD})
    print(f"async #{i}: {r.status_code}")

async def run_async(n=3):
    t0 = time.perf_counter()
    async with httpx.AsyncClient() as client:
        await asyncio.gather(*[one(client, i) for i in range(n)])
    print(f"异步总耗时: {time.perf_counter() - t0:.2f}s")

if __name__ == "__main__":
    run_sync()              # 先跑同步
    asyncio.run(run_async())  # 再跑异步