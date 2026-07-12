from pydantic import BaseModel


class JdAnalyzeRequest(BaseModel):
    jd_text: str


class JdAnalyzeResponse(BaseModel):
    word_count: int
    has_python: bool
    has_ai_keyword: bool
    keywords: list[str]
