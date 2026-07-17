"""3.1 通关测试：用 dependency_overrides 验证四类异常统一格式。

不真调 LLM，靠假 service 注入异常，覆盖 404/422/503/500。
运行：.venv/Scripts/python.exe scripts/test_error_handlers.py
"""
from fastapi.testclient import TestClient

from app.api.dependencies import get_llm_service
from app.core.exceptions import ServiceError
from app.main import app


class FakeTimeoutService:
    """故意抛 ServiceError，模拟上游 LLM 超时/不可用。"""

    async def analyze_jd(self, jd_text: str):
        raise ServiceError(message="上游 LLM 超时/不可用")


class FakeBoomService:
    """故意抛未预料异常，模拟代码 bug。"""

    async def analyze_jd(self, jd_text: str):
        raise ValueError("某个没料到的内部错误")


# raise_server_exceptions=False：服务端未接住的异常也返回 500 响应，
# 而不是在测试端重抛 traceback（否则 500 兜底处理器没法验证）
client = TestClient(app, raise_server_exceptions=False)


def main():
    # 场景 A：404（路由不存在，验证 HTTPException 处理器接管）
    r = client.get("/nope")
    print("404 ->", r.status_code, r.json())

    # 场景 B：422（缺 jd_text，验证 RequestValidationError 处理器接管）
    r = client.post("/api/v1/jd/analyze-basic-llm", json={})
    print("422 ->", r.status_code, r.json())

    # 场景 C：503（注入 FakeTimeoutService，验证 AppException 处理器）
    app.dependency_overrides[get_llm_service] = lambda: FakeTimeoutService()
    r = client.post(
        "/api/v1/jd/analyze-basic-llm",
        json={"jd_text": "招聘 Python 工程师，要求熟悉大模型"},
    )
    print("503 ->", r.status_code, r.json())

    # 场景 D：500（注入 FakeBoomService，验证未预料异常兜底处理器）
    app.dependency_overrides[get_llm_service] = lambda: FakeBoomService()
    r = client.post(
        "/api/v1/jd/analyze-basic-llm",
        json={"jd_text": "招聘 Python 工程师，要求熟悉大模型"},
    )
    print("500 ->", r.status_code, r.json())


if __name__ == "__main__":
    main()
