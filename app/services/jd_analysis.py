import json
from app.schemas.jd import JdAnalysisResult


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
