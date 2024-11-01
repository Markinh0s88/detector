# backend/src/main.py
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, Optional
import jwt
import uvicorn
from datetime import datetime, timedelta

from models.models import Base
from database import engine, SessionLocal
from schemas import *
from services.plate_detector import PlateDetector
from services.camera_service import CameraService

# Criar tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema de Detecção de Placas")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique os domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuração JWT
SECRET_KEY = "seu_secret_key_super_secreto"  # Em produção, use variável de ambiente
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Autenticação
@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    condominium = authenticate_condominium(db, form_data.username, form_data.password)
    if not condominium:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais incorretas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        data={"sub": condominium.id}
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Rotas para veículos
@app.get("/vehicles", response_model=List[VehicleResponse])
async def get_vehicles(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    condominium_id = verify_token(token)
    vehicles = db.query(Vehicle).filter(Vehicle.condominium_id == condominium_id).all()
    return vehicles

@app.post("/vehicles", response_model=VehicleResponse)
async def create_vehicle(
    vehicle: VehicleCreate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    condominium_id = verify_token(token)
    db_vehicle = Vehicle(
        **vehicle.dict(),
        condominium_id=condominium_id
    )
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

# Rotas para configurações
@app.get("/settings", response_model=SettingsResponse)
async def get_settings(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    condominium_id = verify_token(token)
    settings = db.query(Settings).filter(Settings.condominium_id == condominium_id).first()
    if not settings:
        raise HTTPException(status_code=404, detail="Configurações não encontradas")
    return settings

@app.put("/settings", response_model=SettingsResponse)
async def update_settings(
    settings: SettingsUpdate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    condominium_id = verify_token(token)
    db_settings = db.query(Settings).filter(Settings.condominium_id == condominium_id).first()
    if not db_settings:
        raise HTTPException(status_code=404, detail="Configurações não encontradas")
    
    for key, value in settings.dict(exclude_unset=True).items():
        setattr(db_settings, key, value)
    
    db.commit()
    db.refresh(db_settings)
    return db_settings

# Rota para stream da câmera
@app.websocket("/ws/camera")
async def camera_stream(websocket: WebSocket):
    await websocket.accept()
    camera_service = CameraService()
    plate_detector = PlateDetector()
    
    try:
        while True:
            frame = await camera_service.get_frame()
            if frame is not None:
                # Detectar placa
                plates = await plate_detector.detect_plates(frame)
                
                # Enviar frame e resultados para o cliente
                await websocket.send_json({
                    "frame": frame.tolist(),
                    "plates": plates
                })
    except WebSocketDisconnect:
        print("Cliente desconectado")
    finally:
        camera_service.release()

# Rotas para logs de detecção
@app.get("/detection-logs", response_model=List[DetectionLogResponse])
async def get_detection_logs(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
    skip: int = 0,
    limit: int = 100
):
    condominium_id = verify_token(token)
    logs = db.query(DetectionLog)\
        .join(Vehicle)\
        .filter(Vehicle.condominium_id == condominium_id)\
        .offset(skip)\
        .limit(limit)\
        .all()
    return logs

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
