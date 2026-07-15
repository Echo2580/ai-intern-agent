import logging

from fastapi import Depends, FastAPI

from app.api.dependencies import get_settings
from app.api.middleware import log_request_time
from app.api.routes.jd import router as jd_router
from app.core.config import Settings
from app.schemas.common import HealthResponse

root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

if not root_logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    ))
    root_logger.addHandler(handler)


app = FastAPI()
app.include_router(jd_router)
app.middleware("http")(log_request_time)


@app.get("/health", response_model=HealthResponse)
def health(settings: Settings = Depends(get_settings)):
    logger.info("Health check requested")
    # 返回一个 HealthResponse 实例
    return HealthResponse(status="ok", 
                          service="AI Intern Agent", 
                          version="0.1.0", 
                          app_name=settings.APP_NAME, 
                          debug=settings.DEBUG
                          )
