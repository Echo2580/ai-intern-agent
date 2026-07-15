import logging
import time

logger = logging.getLogger(__name__)


async def log_request_time(request, call_next):
    start =time.time()
    response = await call_next(request)
    duration_ms = (time.time() - start) * 1000
    logger.info(f"{request.method} {request.url.path} took {duration_ms:.2f}ms")
    return response