import os
import sys


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from dotenv import load_dotenv
from openai import OpenAI
from app.services.jd_analysis import parse_jd_analysis


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
    return f"""请分析下面的 JD 文本，只输出一个 JSON 对象，不要任何解释或 markdown 标记。
JSON 必须包含以下字段，类型严格如下：
- job_title: str（职位名称）
- required_skills: list[str]（技能要求）
- responsibilities: list[str]（职责）
- keywords: list[str]（关键词）
- difficulty: str（简单/中等/困难）

示例格式：
{{"job_title": "Python工程师", "required_skills": ["Python"], "responsibilities": ["后端开发"], "keywords": ["AI"], "difficulty": "中等"}}

JD 文本：
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

    jd2 = """【机器学习算法工程师】
    职责：负责推荐系统的算法设计与优化，搭建并迭代排序模型，分析业务数据驱动策略。
    要求：熟悉 Python，掌握 PyTorch / TensorFlow，深入理解机器学习与深度学习，
    有大模型微调或 NLP 经验者优先，具备扎实的数学与统计基础。"""

    jd3 = """【前端开发工程师】
    职责：负责公司官网与后台管理系统的前端开发，实现响应式交互界面。
    要求：精通 JavaScript，熟悉 React / Vue，掌握 HTML/CSS，
    了解 Webpack 与前端性能优化，有 TypeScript 经验者优先。"""


    # user_prompt = build_jd_user_prompt(sample_jd)

    # reply = call_llm(
    #     prompt=user_prompt,
    #     system_prompt=SYSTEM_PROMPT_JD,
    #     temperature=0,
    # )
    # print(reply)


    jds = [sample_jd, jd2, jd3]
    ok = 0
    for i, jd in enumerate(jds, 1):
        raw = call_llm(prompt=build_jd_user_prompt(jd), system_prompt=SYSTEM_PROMPT_JD, temperature=0)
        try:
            result = parse_jd_analysis(raw)
            ok += 1
            print(f"JD{i} OK: {result.job_title} / 技能{len(result.required_skills)}个")
        except Exception as e:
            print(f"JD{i} 失败: {type(e).__name__}: {e}")   # 关键：打印错误，不吞掉
    print(f"成功率: {ok}/{len(jds)}")
