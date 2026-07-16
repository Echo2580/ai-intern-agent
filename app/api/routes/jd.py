import logging

from fastapi import APIRouter, Depends

from app.api.dependencies import get_llm_service
from app.schemas.jd import JdAnalysisResult, JdAnalyzeRequest, JdAnalyzeResponse
from app.services.llm_service import LlmService

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


@router.post("/analyze-basic-llm", response_model=JdAnalysisResult)
async def analyze_basic_llm(
    req: JdAnalyzeRequest,
    llm_service: LlmService = Depends(get_llm_service),
):
    logger.info("analyze-basic-llm called, jd_text length=%s", len(req.jd_text))
    return await llm_service.analyze_jd(req.jd_text)
