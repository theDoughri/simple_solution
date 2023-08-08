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

# Dummy DB URL
DUMMY_DATABASE_URL = "sqlite:///./dummy_computers.db"
override_engine = create_engine(DUMMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=override_engine)

def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
'''Test cases:'''

''' Testing creat_new_computer '''
def test_create_new_computer_success():

    idx = 1 # could be used in loop for multiple new computers creation
    # Make a request to the endpoint to add a new computer for an existing employee
    computer_data = {"mac_address": f"00:00:00:00:00:{idx:02d}", 
                        "computer_name": f"PC_{idx:02d}", 
                        "ip_address": f"192.168.0.{idx}",
                        "employee_abbreviation": "ASD", 
                        "description": f"Abdessamad laptop {idx}"
                        }
    response = client.post("/computers/", json=computer_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["mac_address"] == f"00:00:00:00:00:{idx:02d}"
    assert data["computer_name"] == f"PC_{idx:02d}"
    assert data["ip_address"] == f"192.168.0.{idx}"
    assert data["employee_abbreviation"] == "ASD"
    assert data["description"] == f"Abdessamad laptop {idx}"
    assert "id" in data  # Make sure the id created

def test_create_new_computer_employee_abbreviation_too_long():
    # Make a request with an employee abbreviation that is too long
    computer_data = {"mac_address": "00:00:00:00:00:99", 
                    "computer_name": "PC_99", 
                    "ip_address": "192.168.0.99",
                    "employee_abbreviation": "DAS_ASD", 
                    "description": "Abdessamad laptop 99"
                    }
    response = client.post("/computers/", json=computer_data)

    assert response.status_code == 403
    assert response.json() == {"detail": "Employee abbreviation too long"}

def test_create_new_computer_employee_abbreviation_Mac_duplicated():
    # Make a request with an employee duplicated MAC
    computer_data = {"mac_address": "00:00:00:00:00:01", 
                    "computer_name": "PC_99", 
                    "ip_address": "192.168.0.99",
                    "employee_abbreviation": "ASD", 
                    "description": "Abdessamad laptop 99"
                    }
    response = client.post("/computers/", json=computer_data)

    assert response.status_code == 403
    assert response.json() == {"detail": "Could not add the new computer. Ensure MAC address is not duplicated"}

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
    # Let's creat an empty dummy db
    app.dependency_overrides[get_db] = override_get_db
    Base.metadata.create_all(bind=override_engine)
    response = client.get("/computers")
    assert response.status_code == 200
    assert len(response.json()) == 0

    # Reset session maker and remove dummy db file
    app.dependency_overrides[get_db] = get_db
    os.remove("dummy_computers.db")