import logging
import time

from openai import OpenAI

from app.core.config import settings

client = OpenAI(
    api_key=settings.DEEPSEEK_API_KEY,
    base_url=settings.DEEPSEEK_BASE_URL,
)

logger = logging.getLogger(__name__)


def call_llm(
    prompt: str,
    system_prompt: str = "",
    temperature: float = 0,
) -> str:
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
        response = client.chat.completions.create(
            model=settings.LLM_MODEL,
            messages=messages,
            temperature=temperature,
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
