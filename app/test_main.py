import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from starlette.testclient import TestClient
from computer_model import Base
from main import get_db
from main import app
import json
import os

client = TestClient(app)


# Database URL
DATABASE_URL = "sqlite:///./computers.db"
engine = create_engine(DATABASE_URL)

# Dummy DB URL
DATABASE_URL = "sqlite:///./dummy_computers.db"
override_engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=override_engine)

def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


''' Testing get_single_computer '''
def test_get_single_computer_existing():
    # Assume Having at leatst one computer in the test db with id=1
    response = client.get("/computers/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1  # Verify the response contains the correct computer data
    assert json.dumps(data).count("id") == 1  # Make sure we only recieve one computer data 

def test_get_single_computer_not_found():
    # Assume there's no computer with id=99 in the database
    response = client.get("/computers/99")
    assert response.status_code == 404
    assert response.json() == {"detail": "Computer not found"}

''' Testing get_all_computer '''
def test_get_all_computer_existing():
    # Assume Having at leatst one computer in the test db
    response = client.get("/computers")
    assert response.status_code == 200
    data = response.json()
    assert json.dumps(data).count("id") >= 1  # Make sure we recieve at least one computer data

def test_get_all_computer_nothing():
    # Assume we have an empty db
    # Create adummy DB
    app.dependency_overrides[get_db] = override_get_db
    Base.metadata.create_all(bind=override_engine)
    response = client.get("/computers")
    assert response.status_code == 200
    assert len(response.json()) == 0

    # Reset session maker and remove dummy databasse
    app.dependency_overrides[get_db] = get_db
    os.remove("dummy_computers.db")