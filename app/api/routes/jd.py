import logging

from fastapi import APIRouter

from app.schemas.jd import JdAnalyzeRequest, JdAnalyzeResponse

router = APIRouter(prefix="/api/v1/jd", tags=["jd"])
logger = logging.getLogger(__name__)


@router.post("/analyze-basic")
def analyze_basic(req: JdAnalyzeRequest) -> JdAnalyzeResponse:
    logger.info("analyze-basic called, jd_text length=%s", len(req.jd_text))
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

    logger.info(
        "analyze-basic response: word_count=%s, has_python=%s, has_ai_keyword=%s",
        word_count,
        has_python,
        has_ai_keyword,
    )

    return JdAnalyzeResponse(
        word_count=word_count,
        has_python=has_python,
        has_ai_keyword=has_ai_keyword,
        keywords=keywords,
    )
