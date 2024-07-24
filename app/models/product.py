from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship
from datetime import datetime
from app.extensions import db

class Product(db.Model):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    image = Column(LargeBinary, nullable=False)  # Use LargeBinary for binary data
    description = Column(String(250), nullable=False)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship('User', back_populates='products')  # Corrected relationship
    orders = relationship('Order', back_populates='product')
    
    def __init__(self, image, name, description, price, stock, user_id):
        self.image = image
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock
        self.user_id = user_id  # Fixed initialization

    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, price={self.price}, stock={self.stock})>"
