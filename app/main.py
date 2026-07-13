import logging

from fastapi import FastAPI

from app.api.routes.jd import router as jd_router
from app.core.config import settings
from app.schemas.common import HealthResponse

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


app = FastAPI()
app.include_router(jd_router)


@app.get("/health", response_model=HealthResponse)
def health():
    logger.info("Health check requested")
    # 返回一个 HealthResponse 实例
    return HealthResponse(status="ok", 
                          service="AI Intern Agent", 
                          version="0.1.0", 
                          app_name=settings.APP_NAME, 
                          debug=settings.DEBUG
                          )
