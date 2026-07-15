from fastapi.testclient import TestClient

from app.api.dependencies import get_settings
from app.core.config import Settings
from app.main import app


def fake_get_settings():
    return Settings(APP_NAME="Test App", DEBUG=True)


def test_health_with_fake_settings():
    # 覆盖依赖：本来调 get_settings()，现在调 fake_get_settings()
    app.dependency_overrides[get_settings] = fake_get_settings
    try:
        client = TestClient(app)
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["app_name"] == "Test App"
        assert data["debug"] is True
    finally:
        # 必须清理，否则污染其他测试
        app.dependency_overrides.clear()
