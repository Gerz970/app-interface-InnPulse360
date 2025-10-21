from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from services.catalogos.periodicidad_service import PeriodicidadService
from schemas.catalogos.periodicidad_schemas import PeriodicidadCreate, PeriodicidadUpdate, PeriodicidadResponse
from typing import List
from core.database_connection import get_database_session

router = APIRouter(
    prefix="/periodicidades",
    tags=["Periodicidades"]
)

security = HTTPBearer()

@router.get("/", response_model=List[PeriodicidadResponse])
def listar_periodicidades(skip: int = 0, limit: int = 100, db: Session = Depends(get_database_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
    return PeriodicidadService(db).listar(skip, limit)

@router.get("/{id_periodicidad}", response_model=PeriodicidadResponse)
def obtener_periodicidad(id_periodicidad: int, db: Session = Depends(get_database_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
    return PeriodicidadService(db).obtener(id_periodicidad)

@router.post("/", response_model=PeriodicidadResponse, status_code=status.HTTP_201_CREATED)
def crear_periodicidad(data: PeriodicidadCreate, db: Session = Depends(get_database_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
    return PeriodicidadService(db).crear(data)

@router.put("/{id_periodicidad}", response_model=PeriodicidadResponse)
def actualizar_periodicidad(id_periodicidad: int, data: PeriodicidadUpdate, db: Session = Depends(get_database_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
    return PeriodicidadService(db).actualizar(id_periodicidad, data)

@router.delete("/{id_periodicidad}", response_model=PeriodicidadResponse)
def eliminar_periodicidad(id_periodicidad: int, db: Session = Depends(get_database_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
    return PeriodicidadService(db).eliminar(id_periodicidad)
