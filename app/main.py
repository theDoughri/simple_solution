from typing import Optional
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.responses import RedirectResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from messaging import notify_admin
from computer_model import Base
from pydantic import BaseModel

from crud import *

MAX_COMPUTER_BY_USER = 3
MAX_ABREVIATION_LENGHT = 3


# First Let's define a Pydantic model corresponding to the Computer model
class Computer(BaseModel):
    id: Optional[int] = 0 # will be used to update and delete objects
    mac_address: str
    computer_name: str
    ip_address: str
    employee_abbreviation: Optional[str] = None
    description: Optional[str]

# Database URL
DATABASE_URL = "sqlite:///./computers.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

app = FastAPI()

# To ensures that each request gets its own separate database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# For functional testing purpose the root '/' is forward to sawager docs '/doc'
@app.get("/", include_in_schema=False)
def test():
    return RedirectResponse("/docs")

# Add a new computer to an employee
@app.post("/computers/", response_model=Computer)
def create_new_computer(computer_data: dict, db: Session = Depends(get_db)):
    try:
        if "employee_abbreviation" in computer_data and len(computer_data["employee_abbreviation"]) > MAX_ABREVIATION_LENGHT:
            raise HTTPException(status_code=403, detail="Employee abbreviation too long")
        
        computer = create_computer(db, computer_data)
        
        if not computer:
            raise HTTPException(status_code=403, detail="Could not add the new computer. Ensure MAC address is not duplicated")
        
        count = get_computer_count_by_employee(db, computer.employee_abbreviation)
        if count >= MAX_COMPUTER_BY_USER:
            notify_admin(computer.employee_abbreviation, count)
        
        return computer
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

# Get the data of a single computer
@app.get("/computers/{computer_id}", response_model=Computer)
def get_single_computer(computer_id: int, db: Session = Depends(get_db)):
    computer = get_computer(db, computer_id)
    if not computer:
        raise HTTPException(status_code=404, detail="Computer not found")
    return computer

# Get all computers
@app.get("/computers/", response_model=list[Computer])
def get_all_computer(db: Session = Depends(get_db)):
    return get_all_computers(db)

#Get all computers by employee
@app.get("/computers/by-emplyee/{employee_abbreviation}", response_model=list[Computer])
def get_all_computer_by_employee(employee_abbreviation: str, db: Session = Depends(get_db)):
    return get_computers_by_employee(db, employee_abbreviation)

# Update a computer
@app.put("/computers/{computer_id}", response_model=Computer)
def update_existing_computer(computer_id: int, computer_data: dict, db: Session = Depends(get_db)):
    computer = get_computer(db, computer_id)
    try:
        if not computer:
            raise HTTPException(status_code=404, detail="Computer not found")
        updated_computer_data = {k: v for k, v in computer_data.items() if v is not None}
        
        if "employee_abbreviation" in updated_computer_data and len(updated_computer_data["employee_abbreviation"]) > MAX_ABREVIATION_LENGHT:
            raise HTTPException(status_code=403, detail="Employee abbreviation too long")
        
        # Let's check if we have aduplicate MAC adress
        if get_computer_count_by_mac_address(db, updated_computer_data["mac_address"], computer.id):
                raise HTTPException(status_code=403, detail="Could not add the new computer make sure that adresse mac is not duplicated")
        
        if update_computer(db, computer_id, updated_computer_data):
            count = get_computer_count_by_employee(db, updated_computer_data["employee_abbreviation"])
            if count >= MAX_COMPUTER_BY_USER:
                notify_admin(computer.employee_abbreviation, count)
          
        else:
            raise HTTPException(status_code=500, detail="Computer update error")
        return get_computer(db, computer_id)
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


# Remove a computer
@app.delete("/computers/{computer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_computer(computer_id: int, db: Session = Depends(get_db)):
    computer = get_computer(db, computer_id)
    if not computer:
        raise HTTPException(status_code=404, detail="Computer not found")
    delete_computer(db, computer_id)
    return True