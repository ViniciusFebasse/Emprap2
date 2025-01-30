from fastapi.testclient import TestClient
from main import app
import json

client = TestClient(app)

def test_upload():
    file_data = json.dumps([
        {"name": "João Silva", "email": "joao.silva@example.com", "teste": 30},
        {"name": "Maria Oliveira", "email": "maria.oliveira@example.com", "age": 25}
    ])

    response = client.post("/upload/", files={"file": ("users.json", file_data, "application/json")})
    assert response.status_code == 200
    assert "mongo_id" in response.json()
