from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.extensions import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    address = Column(String(200), nullable=False)
    phone_number = Column(String(20), nullable=False)
    role = Column(String(20), default='customer')  # e.g., customer, admin
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Define remaining relationships as needed
    orders = relationship('Order', back_populates='user')
    products = relationship('Product', back_populates='user')

    def __init__(self, name, email, password, address, phone_number, role='customer'):
        self.name = name
        self.email = email
        self.password = password
        self.address = address
        self.phone_number = phone_number
        self.role = role

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, email={self.email}, role={self.role})>"
