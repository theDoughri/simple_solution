import pytest
from starlette.testclient import TestClient
from main import app

client = TestClient(app)


''' Testing get_single_computer '''
def test_get_single_computer_existing():
    # Assume Having at leatst one computer in the test db with id=1
    response = client.get("/computers/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1  # Verify the response contains the correct computer data

def test_get_single_computer_not_found():
    # Assume there's no computer with id=99 in the database
    response = client.get("/computers/99")
    assert response.status_code == 404
    assert response.json() == {"detail": "Computer not found"}
