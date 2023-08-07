from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Computer(Base):
    __tablename__ = 'computers'

    id = Column(Integer, primary_key=True, index=True)
    mac_address = Column(String(17), unique=True, nullable=False)
    computer_name = Column(String, nullable=False)
    ip_address = Column(String(15), nullable=False) #IPv4 only 
    employee_abbreviation = Column(String(3), nullable=True)
    description = Column(String, nullable=True)
