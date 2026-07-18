from app.api.dependencies import get_settings
from app.core.config import Settings
from app.main import app


def fake_get_settings():
    return Settings(APP_NAME="Test App", DEBUG=True)

def test_health_with_fake_settings(client):
    app.dependency_overrides[get_settings] = fake_get_settings
    try:
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["app_name"] == "Test App"
        assert data["debug"] is True
    finally:
        app.dependency_overrides.clear()
