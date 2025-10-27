from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.mantenimiento.mantenimiento_service import MantenimientoService
from schemas.mantenimiento.mantenimiento_schema import MantenimientoCreate, MantenimientoUpdate, MantenimientoResponse
from typing import List
from core.database_connection import get_database_session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

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
