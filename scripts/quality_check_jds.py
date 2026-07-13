import logging

from app.services.jd_analysis import analyze_jd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logging.getLogger("httpx").setLevel(logging.WARNING)




jds = [
    (
        "Python 后端",
        """招聘 Python 后端工程师。
职责：开发和维护 REST API，参与数据库设计与服务部署。
要求：熟练 Python、FastAPI 或 Django，掌握 MySQL、Redis、Docker 和 Linux。""",
    ),
    (
        "机器学习算法",
        """招聘机器学习算法工程师。
职责：优化推荐模型，处理业务数据，迭代排序策略。
要求：掌握 Python、PyTorch 或 TensorFlow，理解机器学习、深度学习和统计学。""",
    ),
    (
        "前端开发",
        """招聘前端开发工程师。
职责：开发管理后台和官网交互页面，持续优化页面性能。
要求：熟练 JavaScript、TypeScript、React 或 Vue，掌握 HTML、CSS 和 Webpack。""",
    ),
    (
        "数据分析",
        """招聘数据分析师。
职责：构建业务报表，分析用户行为并提出数据驱动的建议。
要求：熟练 SQL、Python、Excel，了解 Tableau 或 Power BI，具备沟通能力。""",
    ),
    (
        "产品经理",
        """招聘 AI 产品经理。
职责：调研用户需求，撰写 PRD，协调研发和设计团队推进 AI 功能上线。
要求：具备产品设计、项目管理和数据分析能力，了解 LLM 或 AI 应用。""",
    ),
]

success_count = 0

for index, (name, jd_text) in enumerate(jds, start=1):
    try:
        result = analyze_jd(jd_text)
    except Exception as error:
        print(f"JD {index}（{name}）失败：{type(error).__name__}: {error}")
    else:
        success_count += 1
        print(
            f"JD {index}（{name}）成功："
            f"{result.job_title}，"
            f"技能 {len(result.required_skills)} 个，"
            f"职责 {len(result.responsibilities)} 个"
        )
        print(result.model_dump_json(indent=2))
        print("-" * 60)

print(f"结构化解析成功率：{success_count}/{len(jds)}")
