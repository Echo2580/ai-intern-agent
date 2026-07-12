from fastapi import APIRouter
from app.schemas.jd import JdAnalyzeRequest, JdAnalyzeResponse

router = APIRouter(prefix="/api/v1/jd", tags=["jd"])


@router.post("/analyze-basic")
def analyze_basic(req: JdAnalyzeRequest) -> JdAnalyzeResponse:
    text = req.jd_text
    word_count = len(text)
    has_python = "python" in text.lower()

    keywords = []
    ai_keywords = ["ai", "llm", "大模型", "人工智能", "机器学习"]
    text_lower = text.lower()
    for kw in ai_keywords:
        if kw.lower() in text_lower:
            keywords.append(kw)
    has_ai_keyword = len(keywords) > 0

    return JdAnalyzeResponse(
        word_count=word_count,
        has_python=has_python,
        has_ai_keyword=has_ai_keyword,
        keywords=keywords,
    )
