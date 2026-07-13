import json
import sys
from pathlib import Path

from pydantic import ValidationError

# 将项目根目录加入Python搜索路径，让app模块可导入
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services import jd_analysis

received = {}


def fake_call_llm(
    prompt: str,
    system_prompt: str,
    temperature: float,
) -> str:
    received["prompt"] = prompt
    received["system_prompt"] = system_prompt
    received["temperature"] = temperature

    # 模拟LLM输出：带废话、```json代码围栏（复现线上脏数据场景）
    return """这是模型分析结果：

```json
{
  "job_title": "Python后端工程师",
  "required_skills": ["Python", "FastAPI"],
  "responsibilities": ["开发和维护 REST API"],
  "keywords": ["Python", "FastAPI", "REST API"],
  "difficulty": "中等"
}
"""


# 猴子补丁：替换原始LLM调用
original_call_llm = jd_analysis.call_llm
jd_analysis.call_llm = fake_call_llm

try:
    input_jd = "招聘 Python 后端工程师，要求熟悉 FastAPI。"
    # 修复缩进
    result = jd_analysis.analyze_jd(input_jd)

    # 业务结果断言
    assert result.job_title == "Python后端工程师"
    assert "FastAPI" in result.required_skills
    # 校验传给LLM的温度参数是否为0
    assert received["temperature"] == 0
    # 校验JD原文是否传入prompt
    assert input_jd in received["prompt"]

    print("analyze_jd 假 LLM 测试通过：", result.job_title)
finally:
    # 无论是否报错，都恢复原始函数，避免影响其他代码
    jd_analysis.call_llm = original_call_llm


def failing_call_llm(
    prompt: str,
    system_prompt: str,
    temperature: float,
) -> str:
    raise RuntimeError("模拟 LLM 服务不可用")


jd_analysis.call_llm = failing_call_llm

try:
    jd_analysis.analyze_jd("任意测试 JD")
except RuntimeError as error:
    print("LLM 异常透传测试通过：", error)
else:
    raise AssertionError("LLM 异常不应该被吞掉")
finally:
    jd_analysis.call_llm = original_call_llm


def invalid_json_call_llm(
    prompt: str,
    system_prompt: str,
    temperature: float,
) -> str:
    return '{"job_title": "Python工程师",}'


jd_analysis.call_llm = invalid_json_call_llm

try:
    jd_analysis.analyze_jd("任意测试 JD")
except json.JSONDecodeError:
    print("非法 JSON 异常透传测试通过")
else:
    raise AssertionError("非法 JSON 应该抛出 JSONDecodeError")
finally:
    jd_analysis.call_llm = original_call_llm


def invalid_schema_call_llm(
    prompt: str,
    system_prompt: str,
    temperature: float,
) -> str:
    return """{
        "job_title": "Python工程师",
        "required_skills": "Python, FastAPI",
        "responsibilities": ["后端开发"],
        "keywords": ["Python"],
        "difficulty": "中等"
    }"""


jd_analysis.call_llm = invalid_schema_call_llm

try:
    jd_analysis.analyze_jd("任意测试 JD")
except ValidationError:
    print("字段校验异常透传测试通过")
else:
    raise AssertionError("字段类型错误应该抛出 ValidationError")
finally:
    jd_analysis.call_llm = original_call_llm
