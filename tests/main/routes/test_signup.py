from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_should_return_an_account():
    response = client.post("/api/signup")
    assert response.status_code == 200
