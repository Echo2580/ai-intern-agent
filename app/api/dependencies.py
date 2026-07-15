from app.core.config import Settings, settings
from app.services.llm_service import LlmService


def get_settings() -> Settings:
    return settings

def get_llm_service() -> LlmService:
    return LlmService(settings)