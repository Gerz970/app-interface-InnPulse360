from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.config import Settings
from core.database_connection import get_database_session
from services.hotel.piso_service import PisoService
from schemas.hotel.piso_schema import PisoCreate, PisoUpdate, PisoResponse
from typing import List
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

settings = Settings()
security = HTTPBearer()

router = APIRouter(prefix="/pisos", tags=["Pisos"])

@router.get("/get-by-hotel/{id_hotel}", response_model=List[PisoResponse])
def listar_pisos(id_hotel:int, db: Session = Depends(get_database_session)):
    service = PisoService(db)
    return service.listar_pisos(id_hotel)

@router.get("/{id_piso}", response_model=PisoResponse)
def obtener_piso(id_piso: int, db: Session = Depends(get_database_session)):
    service = PisoService(db)
    try:
        return service.obtener_piso(id_piso)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/", response_model=PisoResponse, status_code=status.HTTP_201_CREATED)
def crear_piso(piso: PisoCreate, db: Session = Depends(get_database_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
    service = PisoService(db)
    return service.crear_piso(piso)

@router.put("/{id_piso}", response_model=PisoResponse)
def actualizar_piso(id_piso: int, piso: PisoUpdate, db: Session = Depends(get_database_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
    service = PisoService(db)
    try:
        return service.actualizar_piso(id_piso, piso)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{id_piso}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_piso(id_piso: int, db: Session = Depends(get_database_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
    service = PisoService(db)
    try:
        service.eliminar_piso(id_piso)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
