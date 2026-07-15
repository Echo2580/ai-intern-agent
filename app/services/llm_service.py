import json
import logging
import time

from openai import OpenAI

from app.core.config import Settings
from app.schemas.jd import JdAnalysisResult

logger = logging.getLogger(__name__)


SYSTEM_PROMPT_JD = """你是一位资深招聘专家，
熟悉当前就业市场以及各类岗位的职责与技能需求。
请用清晰、结构化的中文回答。"""


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


class LlmService:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.client = OpenAI(
            api_key=settings.DEEPSEEK_API_KEY,
            base_url=settings.DEEPSEEK_BASE_URL,
        )


    def call_llm(self,
        prompt: str,
        system_prompt: str = "",
        temperature: float | None = None,
    ) -> str:
        if temperature is None:
            temperature = self.settings.LLM_TEMPERATURE


        messages = []
        if system_prompt:
            messages.append(
                {
                    "role": "system",
                    "content": system_prompt,
                }
            )
        messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        start_time = time.perf_counter()

        try:
            response = self.client.chat.completions.create(
                model=self.settings.LLM_MODEL,
                messages=messages,
                temperature=temperature,
                max_tokens=self.settings.LLM_MAX_TOKENS,
                timeout=self.settings.LLM_TIMEOUT,
            )

            content = response.choices[0].message.content
            if content is None:
                raise ValueError("LLM returned empty content")
        except Exception:
            duration_ms = (time.perf_counter() - start_time) * 1000
            logger.exception(
                "LLM call failed: prompt_length=%s, duration_ms=%.2f",
                len(prompt),
                duration_ms,
            )
            raise

        duration_ms = (time.perf_counter() - start_time) * 1000
        logger.info(
            "LLM call succeeded: prompt_length=%s, duration_ms=%.2f, output_length=%s",
            len(prompt),
            duration_ms,
            len(content),
        )
        return content

    def analyze_jd(self, jd_text: str) -> JdAnalysisResult:
        user_prompt = build_jd_user_prompt(jd_text)
        raw = self.call_llm(
            prompt=user_prompt,
            system_prompt=SYSTEM_PROMPT_JD,
            temperature=0,
        )
        return parse_jd_analysis(raw)


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

