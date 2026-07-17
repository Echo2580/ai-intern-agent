import asyncio
import json
import logging
import random
import time

import openai
from openai import AsyncOpenAI

from app.core.config import Settings
from app.core.exceptions import ServiceError
from app.schemas.jd import JdAnalysisResult

logger = logging.getLogger(__name__)


SYSTEM_PROMPT_JD = """你是一位资深招聘专家，
熟悉当前就业市场以及各类岗位的职责与技能需求。
请用清晰、结构化的中文回答。"""
max_retries = 3


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
        self.client = AsyncOpenAI(
            api_key=settings.DEEPSEEK_API_KEY,
            base_url=settings.DEEPSEEK_BASE_URL,
        )


    async def call_llm(self,
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

        async def _wait_with_backoff(attempt: int, 
                                     base_delay: float = 1.0, 
                                     max_delay: float = 10.0):
            backoff = min(base_delay * (2 ** attempt), max_delay)  # 指数增长，封顶
            jitter = random.uniform(0, backoff)                    # 随机抖动打散同步
            wait = backoff + jitter
            logger.warning("LLM 第 %s 次重试，等待 %.2fs", attempt + 1, wait)
            await asyncio.sleep(wait)                              # 异步等待

        start_time = time.perf_counter()
        
        
        for attempt in range(max_retries):
            try:
                response = await self.client.chat.completions.create(
                    model=self.settings.LLM_MODEL,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=self.settings.LLM_MAX_TOKENS,
                )
                content = response.choices[0].message.content
                if content is None:
                    raise ValueError("LLM returned empty content")
                duration_ms = (time.perf_counter() - start_time) * 1000
                logger.info(
                    "LLM call succeeded: prompt_length=%s, duration_ms=%.2f, output_length=%s",
                    len(prompt),
                    duration_ms,
                    len(content),
                )
                return content                      # 成功：跳出重试循环
            except (openai.RateLimitError, openai.APITimeoutError,
                    openai.APIConnectionError, openai.InternalServerError) as e:
                logger.warning("LLM 可重试异常 %s (第%s次)", type(e).__name__, attempt + 1)
                if attempt == max_retries - 1:
                    raise ServiceError(message="上游 LLM 多次重试仍失败", detail=str(e))
                await _wait_with_backoff(attempt)
                   # 填空：退避等待
                continue
            except openai.AuthenticationError as e:
                raise ServiceError(message="LLM 认证失败，请检查 API Key", detail=str(e))


    async def analyze_jd(self, jd_text: str) -> JdAnalysisResult:
        user_prompt = build_jd_user_prompt(jd_text)
        raw = await self.call_llm(
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

