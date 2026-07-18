from unittest.mock import AsyncMock, Mock

import pytest
from pydantic import ValidationError

from app.core.config import Settings
from app.services.llm_service import LlmService


@pytest.fixture
def llm_service():
    # Settings 必填项用假值；create 马上被 mock 掉，不会真连网络
    settings = Settings(
        DEEPSEEK_API_KEY="test-key",
        DEEPSEEK_BASE_URL="http://test.local",
    )
    return LlmService(settings)


def _make_fake_response(content: str) -> Mock:
    """造一个长得像 OpenAI 返回对象的假 response。"""
    resp = Mock()
    resp.choices = [Mock(message=Mock(content=content))]
    return resp


async def test_analyze_jd_parses_fake_response(llm_service):
    json_str = (
        '{"job_title": "Python工程师",'
        ' "required_skills": ["Python", "FastAPI"],'
        ' "responsibilities": ["后端开发"],'
        ' "keywords": ["AI"],'
        ' "difficulty": "中等"}'
    )
    # ★ mock 点（图里红色层）：替换网络边界 create
    llm_service.client.chat.completions.create = AsyncMock(
        return_value=_make_fake_response(json_str)
    )

    result = await llm_service.analyze_jd("招聘Python工程师")

    assert result.job_title == "Python工程师"
    assert result.required_skills == ["Python", "FastAPI"]
    assert result.keywords == ["AI"]
    assert result.difficulty == "中等"
    # 铁证：确实走了 mock 的 create，且是 await 调用（没真发网络）
    llm_service.client.chat.completions.create.assert_awaited_once()


async def test_analyze_jd_strips_code_fence(llm_service):
    # LLM 常返回 ```json 围栏，验证 clean_json_response 能剥掉
    fenced = (
        "```json\n"
        '{"job_title": "Go工程师", "required_skills": ["Go"],'
        ' "responsibilities": ["服务端"], "keywords": [], "difficulty": "简单"}\n'
        "```"
    )
    llm_service.client.chat.completions.create = AsyncMock(
        return_value=_make_fake_response(fenced)
    )

    result = await llm_service.analyze_jd("招聘Go工程师")
    assert result.job_title == "Go工程师"   # 围栏被剥掉并正确解析


async def test_analyze_jd_invalid_json_raises(llm_service):
    # 合法 JSON 但缺必填字段 -> Pydantic 校验失败
    bad = '{"job_title": "X"}'
    llm_service.client.chat.completions.create = AsyncMock(
        return_value=_make_fake_response(bad)
    )

    with pytest.raises(ValidationError):
        await llm_service.analyze_jd("招聘")
