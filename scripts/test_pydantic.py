from pydantic import ValidationError

from app.schemas.common import HealthResponse

health_response = HealthResponse(
    status="ok",
    service="ai-intern-agent",
)
print(health_response.model_dump())
try:
    bad_response = HealthResponse(
      status=["not", "a", "string"],
      service="ai-intern-agent",
    )

    print(bad_response.model_dump())
except ValidationError as error:
    print("有错误:")
    print(error)