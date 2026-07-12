from pydantic import BaseModel


class JdAnalyzeRequest(BaseModel):
    jd_text: str


class JdAnalyzeResponse(BaseModel):
    word_count: int
    has_python: bool
    has_ai_keyword: bool
    keywords: list[str]


class JdAnalysisResult(BaseModel):
    job_title: str
    required_skills: list[str]
    responsibilities: list[str]
    keywords: list[str]
    difficulty: str
