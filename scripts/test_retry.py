import asyncio
from types import SimpleNamespace

import openai

from app.core.exceptions import ServiceError
from app.services.llm_service import LlmService


class FakeSettings:
    DEEPSEEK_API_KEY = "fake"
    DEEPSEEK_BASE_URL = "https://fake"
    LLM_MODEL = "fake"
    LLM_TEMPERATURE = 0
    LLM_MAX_TOKENS = 100


def make_response(content: str):
    # 造一个和 openai 返回结构一致的假对象：resp.choices[0].message.content
    return SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content=content))]
    )


async def test_retry_then_success():
    service = LlmService(FakeSettings())
    call_count = 0

    async def fake_create(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise openai.APITimeoutError("模拟超时")
        return make_response("OK")

    service.client.chat.completions.create = fake_create  # 偷换底层调用
    result = await service.call_llm("测试 prompt")
    print(f"[场景A] 重试后成功: 调用次数={call_count}, 返回={result}")
    assert call_count == 3, "应当重试2次后第3次成功"


async def test_retry_exhausted():
    service = LlmService(FakeSettings())

    async def fake_create(*args, **kwargs):
        raise openai.APITimeoutError("一直超时")

    service.client.chat.completions.create = fake_create
    try:
        await service.call_llm("测试 prompt")
        print("[场景B] ❌ 应该抛 ServiceError 但没抛")
    except ServiceError as e:
        print(f"[场景B] 重试耗尽正确抛出 ServiceError: {e.message}")


if __name__ == "__main__":
    asyncio.run(test_retry_then_success())
    asyncio.run(test_retry_exhausted())
