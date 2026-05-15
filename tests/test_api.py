from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Dog Breed Classification API!"}

def test_model_info():
    response = client.get("/model_info")
    assert response.status_code == 200
    