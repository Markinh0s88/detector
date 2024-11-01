# backend/src/models/models.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Condominium(Base):
    __tablename__ = "condominiums"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    password_hash = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    settings = relationship("Settings", back_populates="condominium", uselist=False)
    vehicles = relationship("Vehicle", back_populates="condominium")

class Settings(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)
    condominium_id = Column(Integer, ForeignKey("condominiums.id"))
    camera_ip = Column(String)
    camera_port = Column(String)
    camera_username = Column(String)
    camera_password = Column(String)
    camera_stream_path = Column(String)
    enable_sound = Column(Boolean, default=True)
    success_volume = Column(Integer, default=80)
    error_volume = Column(Integer, default=70)
    detection_confidence = Column(Float, default=0.8)
    min_plate_size = Column(Integer, default=100)
    max_plate_size = Column(Integer, default=1000)
    
    condominium = relationship("Condominium", back_populates="settings")

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    condominium_id = Column(Integer, ForeignKey("condominiums.id"))
    plate_number = Column(String, index=True)
    owner_name = Column(String)
    apartment = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    condominium = relationship("Condominium", back_populates="vehicles")
    detection_logs = relationship("DetectionLog", back_populates="vehicle")

class DetectionLog(Base):
    __tablename__ = "detection_logs"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    detected_at = Column(DateTime, default=datetime.utcnow)
    confidence = Column(Float)
    image_path = Column(String, nullable=True)
    
    vehicle = relationship("Vehicle", back_populates="detection_logs")
