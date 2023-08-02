from sqlalchemy.orm import Session
from computer_model import Computer

def create_computer(db: Session, computer_data: dict):
    computer = Computer(**computer_data)
    if get_computer_by_mac_adress(db, computer.mac_address):
        # print("Mac adress already exists")
        return None
    db.add(computer)
    db.commit()
    db.refresh(computer)
    return computer

def get_computer(db: Session, computer_id: int):
    return db.query(Computer).filter(Computer.id == computer_id).first()

def get_computer_by_mac_adress(db: Session, mac_address: str):
    return db.query(Computer).filter(Computer.mac_address == mac_address).first()

def get_all_computers(db: Session):
    return db.query(Computer).all()

def update_computer(db: Session, computer_id: int, computer_data: dict):
    db.query(Computer).filter(Computer.id == computer_id).update(computer_data)
    db.commit()
    return True

def delete_computer(db: Session, computer_id: int):
    db.query(Computer).filter(Computer.id == computer_id).delete()
    db.commit()
    return True

def get_computer_count_by_employee(db: Session, employee_abbreviation: str):
    return db.query(Computer).filter(Computer.employee_abbreviation == employee_abbreviation).count()

def get_computers_by_employee(db: Session, employee_abbreviation: str):
    return db.query(Computer).filter(Computer.employee_abbreviation == employee_abbreviation)

def get_computer_count_by_mac_address(db: Session, mac_address: str, exclude: int = 0):
    return db.query(Computer).filter(Computer.mac_address == mac_address, Computer.id != exclude).count()