from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from services.mantenimiento.mantenimiento_service import MantenimientoService
from schemas.mantenimiento.mantenimiento_schema import MantenimientoCreate, MantenimientoUpdate, MantenimientoResponse
from typing import List
from core.database_connection import get_database_session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime

router = APIRouter(prefix="/mantenimientos", tags=["Mantenimientos"])
service = MantenimientoService()
security = HTTPBearer()

@router.get("/", response_model=List[MantenimientoResponse])
def listar_mantenimientos(db: Session = Depends(get_database_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
    return service.obtener_todos(db)

@router.get("/{id_mantenimiento}", response_model=MantenimientoResponse)
def obtener_mantenimiento(id_mantenimiento: int, db: Session = Depends(get_database_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
    mantenimiento = service.obtener_por_id(db, id_mantenimiento)
    if not mantenimiento:
        raise HTTPException(status_code=404, detail="Mantenimiento no encontrado")
    return mantenimiento

@router.post("/", response_model=MantenimientoResponse)
def crear_mantenimiento(data: MantenimientoCreate, db: Session = Depends(get_database_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
    return service.crear(db, data)

@router.put("/{id_mantenimiento}", response_model=MantenimientoResponse)
def actualizar_mantenimiento(id_mantenimiento: int, data: MantenimientoUpdate, db: Session = Depends(get_database_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
    mantenimiento = service.actualizar(db, id_mantenimiento, data)
    if not mantenimiento:
        raise HTTPException(status_code=404, detail="Mantenimiento no encontrado")
    return mantenimiento

@router.delete("/{id_mantenimiento}", response_model=MantenimientoResponse)
def eliminar_mantenimiento(id_mantenimiento: int, db: Session = Depends(get_database_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
    mantenimiento = service.eliminar(db, id_mantenimiento)
    if not mantenimiento:
        raise HTTPException(status_code=404, detail="Mantenimiento no encontrado")
    return mantenimiento

@router.get("/fecha/", response_model=List[MantenimientoResponse])
def obtener_por_fecha(
    fecha_inicio: datetime = Query(..., description="Fecha exacta de inicio del mantenimiento (YYYY-MM-DD)"),
    db: Session = Depends(get_database_session),
    credentials: HTTPAuthorizationCredentials = Depends(security)):
    mantenimientos = service.obtener_por_fecha(db, fecha_inicio)
    if not mantenimientos:
        raise HTTPException(status_code=404, detail="No se encontraron mantenimientos para esa fecha")
    return mantenimientos

@router.get("/empleado/{empleado_id}", response_model=List[MantenimientoResponse])
def obtener_por_empleado(
    empleado_id: int,
    db: Session = Depends(get_database_session),
    credentials: HTTPAuthorizationCredentials = Depends(security)):
    mantenimientos = service.obtener_por_empleado(db, empleado_id)
    if not mantenimientos:
        raise HTTPException(status_code=404, detail="No se encontraron mantenimientos para este empleado")
    return mantenimientos

@router.get("/empleado-fecha/{empleado_id}", response_model=List[MantenimientoResponse])
def obtener_por_empleado(
    empleado_id: int,
    fecha_inicio: datetime = Query(..., description="Fecha exacta de inicio del mantenimiento (YYYY-MM-DD)"),
    db: Session = Depends(get_database_session),
    credentials: HTTPAuthorizationCredentials = Depends(security)):
    mantenimientos = service.obtener_por_empleado_fecha(db, empleado_id, fecha_inicio)
    if not mantenimientos:
        raise HTTPException(status_code=404, detail="No se encontraron mantenimientos para este empleado")
    return mantenimientos