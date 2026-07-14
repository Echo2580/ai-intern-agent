# AI Intern Agent

基于 FastAPI 和 LLM 的 JD 分析练习项目。

## 技术栈
- Python、FastAPI、Pydantic、OpenAI SDK、Ruff

## 快速开始
1. `git clone <仓库地址>`
2. `cd ai-intern-agent`
3. 创建并激活虚拟环境
4. `pip install -r requirements.txt`
5. 配置 `.env` 后运行 `uvicorn app.main:app --reload`

## 环境变量配置
```env
DEEPSEEK_API_KEY=你的密钥
DEEPSEEK_BASE_URL=服务地址
LLM_MODEL=deepseek-chat
```

## 接口示例：
```bash
curl http://127.0.0.1:8000/health
curl -X POST http://127.0.0.1:8000/api/v1/jd/analyze-basic ^
  -H "Content-Type: application/json" ^
  -d "{\"jd_text\":\"招聘 Python 后端工程师，要求熟悉 FastAPI。\"}"
  ```

## 项目结构
```
app/
├── main.py          # 创建应用、注册路由
├── api/routes/      # HTTP 路由
├── schemas/         # 请求与响应模型
├── services/        # JD 分析、LLM 调用
└── core/            # 配置
```