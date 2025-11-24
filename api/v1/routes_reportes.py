from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.config import Settings
from core.database_connection import get_database_session
from typing import List
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import date
from services.reportes.reportes_service import ResportesService
from fastapi import Path

settings = Settings()
security = HTTPBearer()

router = APIRouter(prefix="/reportes", tags=["Reportes"])

@router.get("/get-entradas-tipo-dia/{dia}")
def obtener_entradas_tipo_dia(
    dia: date = Path(
        ..., 
        example="2025-11-23", 
        description="Fecha en formato YYYY-MM-DD"
    ),
    db: Session = Depends(get_database_session)):
    service = ResportesService(db)
    try:
        return service.obtener_entradas_tipo_dia(dia)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    

@router.get("/get-limpiezas-por-empleado/{fecha_inicio}/{fecha_fin}")
def obtener_limpiezas_por_empleado(
    fecha_inicio: date = Path(
        ..., 
        example="2025-11-23", 
        description="Fecha en formato YYYY-MM-DD"
    ),
    fecha_fin: date = Path(
        ..., 
        example="2025-11-24", 
        description="Fecha en formato YYYY-MM-DD"
    ),
    db: Session = Depends(get_database_session)):
    service = ResportesService(db)
    try:
        return service.obtener_limpiezas_por_empleado(fecha_inicio, fecha_fin)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/get-limpiezas-por-tipo-estatus/{fecha_inicio}/{fecha_fin}/{estatus}")
def obtener_limpiezas_por_tipo_por_estatus(
    fecha_inicio: date = Path(
        ..., 
        example="2025-11-23", 
        description="Fecha en formato YYYY-MM-DD"
    ),
    fecha_fin: date = Path(
        ..., 
        example="2025-11-24", 
        description="Fecha en formato YYYY-MM-DD"
    ),
    estatus: int = Path(
        ..., 
        example="3", 
        description="1. Pendiente, 2. En progreso, 3. Completada, 4. Cancelada"
    ),
    db: Session = Depends(get_database_session)):
    service = ResportesService(db)
    try:
        return service.obtener_limpiezas_por_tipo_por_estatus(fecha_inicio, fecha_fin, estatus)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))