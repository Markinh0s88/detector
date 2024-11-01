# backend/src/schemas.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    condominium_id: Optional[int] = None

# Condominium Schemas
class CondominiumBase(BaseModel):
    name: str

class CondominiumCreate(CondominiumBase):
    password: str

class CondominiumResponse(CondominiumBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

# Settings Schemas
class SettingsBase(BaseModel):
    camera_ip: Optional[str] = None
    camera_port: Optional[str] = None
    camera_username: Optional[str] = None
    camera_password: Optional[str] = None
    camera_stream_path: Optional[str] = None
    enable_sound: Optional[bool] = None
    success_volume: Optional[int] = Field(None, ge=0, le=100)
    error_volume: Optional[int] = Field(None, ge=0, le=100)
    detection_confidence: Optional[float] = Field(None, ge=0, le=1)
    min_plate_size: Optional[int] = None
    max_plate_size: Optional[int] = None

class SettingsUpdate(SettingsBase):
    pass

class SettingsResponse(SettingsBase):
    id: int
    condominium_id: int

    class Config:
        orm_mode = True

# Vehicle Schemas
class VehicleBase(BaseModel):
    plate_number: str
    owner_name: str
    apartment: str
    is_active: Optional[bool] = True

class VehicleCreate(VehicleBase):
    pass

class VehicleUpdate(VehicleBase):
    pass

class VehicleResponse(VehicleBase):
    id: int
    condominium_id: int
    created_at: datetime

    class Config:
        orm_mode = True

# Detection Log Schemas
class DetectionLogBase(BaseModel):
    confidence: float
    image_path: Optional[str] = None

class DetectionLogCreate(DetectionLogBase):
    vehicle_id: int

class DetectionLogResponse(DetectionLogBase):
    id: int
    vehicle_id: int
    detected_at: datetime
    vehicle: VehicleResponse

    class Config:
        orm_mode = True

# Plate Detection Response
class PlateDetection(BaseModel):
    plate_number: str
    confidence: float
    bbox: List[int]
    is_registered: bool
    vehicle: Optional[VehicleResponse] = None
