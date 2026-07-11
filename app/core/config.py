from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DEEPSEEK_API_KEY: str
    DEEPSEEK_BASE_URL: str
    LLM_MODEL: str = "deepseek-chat"
    APP_NAME: str = "AI Intern Agent"
    DEBUG: bool = False

settings = Settings()
