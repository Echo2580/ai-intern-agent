import os

from dotenv import load_dotenv
from openai import OpenAI


# 这是一个常量，整个文件里不变
SYSTEM_PROMPT_JD = """你是一位资深招聘专家，熟悉当前就业市场以及各类岗位的职责与技能需求。请用清晰、结构化的中文回答。"""

load_dotenv()

api_key = os.getenv("DEEPSEEK_API_KEY")
base_url = os.getenv("DEEPSEEK_BASE_URL")
model = os.getenv("LLM_MODEL")

client = OpenAI(
    api_key=api_key,
    base_url=base_url,
)


def call_llm(
    prompt: str,
    system_prompt: str = "",
    temperature: float = 0.7,
) -> str:
    messages = []

    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})

    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content


def chat(messages: list[dict]) -> str:
    response = client.chat.completions.create(
        model=model,
        messages=messages,
    )
    return response.choices[0].message.content


# 这是一个函数，每次把 JD 文本填进去
def build_jd_user_prompt(jd_text: str) -> str:
    
    return f"""请分析下面这段文本，提取出关键信息，并且输出包含职位名称，技能要求，职责，关键词四个部分
{jd_text}
    """


if __name__ == "__main__":
#     reply = call_llm(
#       prompt="请用一句话描述什么是 AI Agent",
#       system_prompt="You are a helpful assistant.",
#       temperature=1,
#     )
#     print(reply)
#     messages = [
#     {"role": "system", "content": "You are a helpful assistant."},
#     {"role": "user", "content": "什么是 RAG？"},
# ]
#     first_reply = chat(messages)
#     print(first_reply)
#     messages.append({"role": "assistant", "content": first_reply})
#     messages.append({"role": "user", "content": "它和微调有什么区别？"})
#     second_reply = chat(messages)
#     print(second_reply)
    sample_jd = """【Python 后端开发工程师】
    职责：负责公司核心业务系统的后端开发，设计与维护 REST API。
    要求：精通 Python，熟悉 FastAPI / Django，掌握 MySQL 与 Redis，
    了解 Docker 与 Linux 部署，有高并发经验者优先。"""

    user_prompt = build_jd_user_prompt(sample_jd)

    reply = call_llm(
        prompt=user_prompt,
        system_prompt=SYSTEM_PROMPT_JD,
        temperature=0,
    )
    print(reply)
