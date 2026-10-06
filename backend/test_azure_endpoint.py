from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

response = client.get("/sentiment/azure-test?text=I+love+this+product")
print("Status Code:", response.status_code)
print("Response JSON:", response.json())
