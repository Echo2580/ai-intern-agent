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

# TODO: 调用 client.chat.completions.create(...)
# 提示：
# model 用上面的 model
# messages 放一个 user 消息
# user content 写：你好，请用一句话介绍你自己
# 最后 print 出模型回复
response = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "你好，请用一句话介绍你自己"},
    ],
)

print(response.choices[0].message.content)