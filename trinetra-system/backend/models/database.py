from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(String, primary_key=True)
    face_encoding = Column(String)  # Store face encoding as base64 string
    first_visit = Column(DateTime, default=datetime.utcnow)
    last_visit = Column(DateTime, default=datetime.utcnow)
    visit_count = Column(Integer, default=1)
    transactions = relationship("Transaction", back_populates="customer")
    emotions = relationship("EmotionRecord", back_populates="customer")

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True)
    customer_id = Column(String, ForeignKey('customers.id'))
    timestamp = Column(DateTime, default=datetime.utcnow)
    total_amount = Column(Float)
    items = Column(String)  # Store as JSON string
    customer = relationship("Customer", back_populates="transactions")

class EmotionRecord(Base):
    __tablename__ = "emotion_records"
    
    id = Column(Integer, primary_key=True)
    customer_id = Column(String, ForeignKey('customers.id'))
    timestamp = Column(DateTime, default=datetime.utcnow)
    emotions = Column(String)  # Store as JSON string
    customer = relationship("Customer", back_populates="emotions")

class Vehicle(Base):
    __tablename__ = "vehicles"
    
    id = Column(Integer, primary_key=True)
    license_plate = Column(String, unique=True)
    first_seen = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow)
    visit_count = Column(Integer, default=1)
    customer_id = Column(String, ForeignKey('customers.id'), nullable=True)

class Camera(Base):
    __tablename__ = "cameras"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)  # entrance, store, billing, parking
    source = Column(String)  # URL or device ID
    is_active = Column(Boolean, default=True)
    last_active = Column(DateTime)
