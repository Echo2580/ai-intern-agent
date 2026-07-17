from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.exceptions import AppException, ErrorResponse


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.code,
        content=ErrorResponse(code=exc.code, message=exc.message, detail=exc.detail).model_dump(),
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
        code=exc.status_code,
        message=str(exc.detail),
        detail=None,
    ).model_dump(),

    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(code=500, 
                              message="服务器内部错误", detail=None
                              ).model_dump(),
    )


async def validation_exception_handler(request: Request,
                                    exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content=ErrorResponse(code=422, 
                              message="请求参数校验失败", detail=exc.errors()).model_dump(),
    )
