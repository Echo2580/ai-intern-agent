def test_analyze_basic_normal(client):
    jd_text = "招聘 Python 后端工程师，要求熟悉 FastAPI 和 AI。"
    response = client.post("/api/v1/jd/analyze-basic", json={"jd_text": jd_text})
    assert response.status_code == 200

    data = response.json()
    assert data["word_count"] == len(jd_text)
    assert data["has_python"] is True
    assert data["has_ai_keyword"] is True
    assert "ai" in data["keywords"]


def test_analyze_basic_missing_jd_text(client):
    response = client.post("/api/v1/jd/analyze-basic", json={})
    assert response.status_code == 422


def test_analyze_basic_empty_jd_text(client):
    response = client.post("/api/v1/jd/analyze-basic", json={"jd_text": ""})
    assert response.status_code == 200

    data = response.json()
    assert data["word_count"] == 0
    assert data["has_python"] is False
    assert data["has_ai_keyword"] is False
    assert data["keywords"] == []


def test_analyze_basic_long_jd_text(client):
    jd_text = "Python " * 1000
    response = client.post("/api/v1/jd/analyze-basic", json={"jd_text": jd_text})
    assert response.status_code == 200

    data = response.json()
    assert data["word_count"] == len(jd_text)
    assert data["has_python"] is True
