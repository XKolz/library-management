from fastapi.testclient import TestClient

client = TestClient()
def test_add_book():
    response = client.post("/books", json={"title": "New Book", "publisher": "Wiley", "category": "Technology"})
    assert response.status_code == 201
