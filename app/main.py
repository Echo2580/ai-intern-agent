from fastapi import FastAPI
from app.core.config import settings
from app.schemas.common import HealthResponse
from app.api.routes.jd import router as jd_router


app = FastAPI()
app.include_router(jd_router)



@app.get("/health", response_model=HealthResponse)
def health():
    # 返回一个 HealthResponse 实例
    return HealthResponse(status="ok", service="AI Intern Agent", version="0.1.0", app_name=settings.APP_NAME, debug=settings.DEBUG)
