import logging

from fastapi import Depends, FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.dependencies import get_settings
from app.api.error_handlers import (
    app_exception_handler,
    http_exception_handler,
    unhandled_exception_handler,
    validation_exception_handler,
)
from app.api.middleware import log_request_time
from app.api.routes.jd import router as jd_router
from app.core.config import Settings
from app.core.exceptions import AppException
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
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)


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
