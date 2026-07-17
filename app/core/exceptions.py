from pydantic import BaseModel


class AppException(Exception):
    def __init__(self, code: int, message: str, detail: object = None):
        self.code = code          # 存成实例属性，处理器靠这个读
        self.message = message
        self.detail = detail
        super().__init__(message)  # 让父类也存 message，没处理器时 print(e) 也有内容

class NotFoundException(AppException):
    def __init__(self, message="资源不存在", detail=None):
        super().__init__(code=404, message=message, detail=detail)  # code 写死 404

class ValidationError(AppException):

    def __init__(self, message="参数验证错误", detail=None):
        super().__init__(code=422, message=message, detail=detail)

class ServiceError(AppException):

    def __init__(self, message="上游 LLM 超时/不可用", detail=None):
        super().__init__(code=503, message=message, detail=detail)

class ErrorResponse(BaseModel):
    code: int
    message: str
    detail: object | None = None
