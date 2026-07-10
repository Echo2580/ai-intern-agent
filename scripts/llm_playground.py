import os

from dotenv import load_dotenv
from openai import OpenAI


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


if __name__ == "__main__":
    reply = call_llm(
      prompt="请用一句话描述什么是 AI Agent",
      system_prompt="You are a helpful assistant.",
      temperature=1,
    )
    print(reply)
    messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "什么是 RAG？"},
]
    first_reply = chat(messages)
    print(first_reply)
    messages.append({"role": "assistant", "content": first_reply})
    messages.append({"role": "user", "content": "它和微调有什么区别？"})
    second_reply = chat(messages)
    print(second_reply)
    

