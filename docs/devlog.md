# 开发日志

## 阶段 1：Python 工程基础 + Agent 概念入门

### 1.1 项目骨架
- 学了什么：创建 Python 项目骨架，使用虚拟环境和 `requirements.txt` 管理依赖，并初始化 Git 仓库。
- 遇到的问题：包初始化文件被命名为 `_init_.py`，目前依赖 namespace package 才能导入；`requirements.txt` 的编码也需要在后续整理时统一检查。
- 验证方式：项目可以从虚拟环境运行，Git 历史保留了初始化提交 `fd3b588`。

### 1.2 Agent 概念与第一次 LLM 调用
- 学了什么：区分普通 LLM 对话与 Agent 的基本概念；通过 `.env` 管理 API Key，并使用 OpenAI 兼容 SDK 调用模型。
- 验证方式：提交 `f050131` 增加 LLM 演示脚本，项目配置不将密钥写入代码。

### 2.1 类型注解与 Pydantic
- 学了什么：为函数补充返回类型注解，使用 Pydantic 模型约束请求和响应的数据形状。
- 验证方式：提交 `66d7367`；后续 JD 解析使用 `JdAnalysisResult.model_validate()` 进行结构校验。

### 2.2 LLM 调用封装
- 学了什么：将模型调用封装为独立能力，理解 `system`、`user` 消息和 `temperature` 对输出稳定性的影响。
- 验证方式：LLM 调用层最终沉淀为 `app/services/llm_service.py`，结构化抽取使用 `temperature=0`。

### 3.1 配置管理与健康检查
- 学了什么：使用 `pydantic-settings` 集中读取环境变量，并创建 FastAPI `GET /health` 接口。
- 遇到的问题：`BaseSettings` 不会自动读取 `.env`，需要通过 `SettingsConfigDict(env_file=".env")` 显式声明。
- 验证方式：提交 `20c6981`；`/health` 使用 `HealthResponse` 约束响应结构。

### 3.2 Prompt 设计
- 学了什么：将角色与全局规则放入 System Prompt，将每次的 JD 文本放入 User Prompt；使用模板函数构建结构化输出要求。
- 验证方式：提交 `88894c9`；JD 分析链路复用 `build_jd_user_prompt()` 和 `SYSTEM_PROMPT_JD`。

### 4.1 FastAPI 路由与请求校验
- 学了什么：使用 `APIRouter` 将 JD 路由与应用入口分离，使用 Pydantic 校验 POST 请求和响应。
- 验证方式：提交 `c4a3895`；`POST /api/v1/jd/analyze-basic` 接收 `JdAnalyzeRequest` 并返回 `JdAnalyzeResponse`。

### 4.2 JSON 清洗与 Pydantic 校验
- 学了什么：从模型原始文本中提取 JSON，使用 `json.loads()` 解析，再用 Pydantic 验证字段类型。
- 遇到的问题：模型可能返回 Markdown 围栏、非法 JSON，或返回结构正确但字段类型错误的数据。
- 验证方式：提交 `7b0967e`；3 段 JD 结构化解析成功率为 3/3。

### 5.1 Ruff、pre-commit 与日志
- 学了什么：使用 Ruff 做静态检查，使用 pre-commit 在提交前自动拦截问题，并用 logging 记录业务事件。
- 遇到的问题：Ruff 能检查未使用导入和排序，但不覆盖所有空白字符问题，`git diff --check` 仍有必要。
- 验证方式：提交 `7e54e08` 和 `19f82a2`；`ruff check .` 已通过，健康检查和基础 JD 接口均有日志。

### 5.2 LLM JD 分析完整链路
- 学了什么：将 Prompt、LLM 调用、JSON 清洗、Pydantic 校验串为 `analyze_jd(jd_text) -> JdAnalysisResult`，并将通用模型调用与 JD 业务编排拆分到不同 service。
- 遇到的问题：自动化测试不能依赖真实模型，否则结果会波动且消耗额度；JSON 解析错误、Schema 校验错误和内容理解错误也需要分开判断。
- 验证方式：提交 `497367f`；固定假响应覆盖正常结果、Markdown JSON、非法 JSON、Pydantic 校验失败和 LLM 异常；5 段真实 JD 质量检查为 5/5；`ruff check .` 通过。
- 后续改进：当前 `required_skills` 会将“FastAPI 或 Django”这类候选关系扁平化，未来可考虑增加技能分组字段。
