import json

from app.schemas.jd import JdAnalysisResult
from app.services.llm_service import call_llm

SYSTEM_PROMPT_JD = """你是一位资深招聘专家，
熟悉当前就业市场以及各类岗位的职责与技能需求。
请用清晰、结构化的中文回答。"""


def build_jd_user_prompt(jd_text: str) -> str:
    return f"""请分析下面的 JD 文本，只输出一个 JSON 对象，不要任何解释或 markdown 标记。
JSON 必须包含以下字段，类型严格如下：
- job_title: str（职位名称）
- required_skills: list[str]（技能要求）
- responsibilities: list[str]（职责）
- keywords: list[str]（关键词）
- difficulty: str（简单/中等/困难）

示例格式：
{{"job_title": "Python工程师",
 "required_skills": ["Python"],
   "responsibilities": ["后端开发"],
   "keywords": ["AI"],
   "difficulty": "中等"}}

JD 文本：
{jd_text}
"""


def clean_json_response(text: str) -> str:
    """清洗 LLM 返回的 JSON 文本：去掉 ```json 代码围栏和前后废话，截出纯 JSON。

    思路：JSON 对象一定被 { 和 } 包着，找第一个 { 和最后一个 } 切出来即可。
    """
    text = text.strip()
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end < start:
        raise ValueError("响应里找不到 JSON 对象")
    return text[start : end + 1]


def parse_jd_analysis(raw: str) -> JdAnalysisResult:
    """完整链路：清洗 -> json.loads -> Pydantic 校验。校验失败抛 ValidationError。"""
    clean = clean_json_response(raw)
    data = json.loads(clean)
    return JdAnalysisResult.model_validate(data)


def analyze_jd(jd_text: str) -> JdAnalysisResult:
    user_prompt = build_jd_user_prompt(jd_text)

    raw_response = call_llm(
        prompt=user_prompt,
        system_prompt=SYSTEM_PROMPT_JD,
        temperature=0,
    )
    return parse_jd_analysis(raw_response)
