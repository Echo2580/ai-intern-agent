from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

health_response = client.get("/health")
assert health_response.status_code == 200
assert health_response.json()["status"] == "ok"

basic_response = client.post(
    "/api/v1/jd/analyze-basic",
    json={"jd_text": "招聘 Python 开发工程师，要求了解 AI。"},
)
assert basic_response.status_code == 200
assert basic_response.json()["has_python"] is True

invalid_response = client.post("/api/v1/jd/analyze-basic", json={})
assert invalid_response.status_code == 422

print("API 测试通过：health=200，analyze-basic=200，缺少 jd_text=422")