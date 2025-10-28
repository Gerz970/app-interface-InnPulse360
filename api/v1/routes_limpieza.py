from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from schemas.camarista.limpieza_schema import LimpiezaCreate, LimpiezaUpdate, LimpiezaResponse
from services.camarista.limpieza_service import LimpiezaService
from core.database_connection import get_database_session
from typing import List
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime

router = APIRouter(prefix="/limpiezas", tags=["Limpiezas"])
service = LimpiezaService()
security = HTTPBearer()

@router.get("/", response_model=List[LimpiezaResponse])
def obtener_limpiezas(db: Session = Depends(get_database_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
    return service.obtener_todos(db)

@router.get("/{id_limpieza}", response_model=LimpiezaResponse)
def obtener_limpieza(id_limpieza: int, db: Session = Depends(get_database_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
    limpieza = service.obtener_por_id(db, id_limpieza)
    if not limpieza:
        raise HTTPException(status_code=404, detail="Limpieza no encontrada o eliminada")
    return limpieza

@router.post("/", response_model=LimpiezaResponse)
def crear_limpieza(data: LimpiezaCreate, db: Session = Depends(get_database_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
    return service.crear(db, data)

@router.put("/{id_limpieza}", response_model=LimpiezaResponse)
def actualizar_limpieza(id_limpieza: int, data: LimpiezaUpdate, db: Session = Depends(get_database_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
    limpieza_actualizada = service.actualizar(db, id_limpieza, data)
    if not limpieza_actualizada:
        raise HTTPException(status_code=404, detail="Limpieza no encontrada o eliminada")
    return limpieza_actualizada

@router.delete("/{id_limpieza}")
def eliminar_limpieza(id_limpieza: int, db: Session = Depends(get_database_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
    limpieza_eliminada = service.eliminar(db, id_limpieza)
    if not limpieza_eliminada:
        raise HTTPException(status_code=404, detail="Limpieza no encontrada")
    return {"message": "Limpieza marcada como eliminada (estatus_limpieza_id = 4)"}

@router.get("/empleado/{empleado_id}", response_model=List[LimpiezaResponse])
def obtener_por_empleado(empleado_id: int, db: Session = Depends(get_database_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
    return service.obtener_por_empleado(db, empleado_id)

@router.get("/habitacion-area/{habitacion_area_id}", response_model=List[LimpiezaResponse])
def obtener_por_habitacion_area(habitacion_area_id: int, db: Session = Depends(get_database_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
    return service.obtener_por_habitacion_area(db, habitacion_area_id)

@router.get("/estatus/{estatus_limpieza_id}", response_model=List[LimpiezaResponse])
def obtener_por_estatus(estatus_limpieza_id: int, db: Session = Depends(get_database_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
    return service.obtener_por_estatus(db, estatus_limpieza_id)

@router.get("/fecha/", response_model=List[LimpiezaResponse])
def obtener_por_fecha(fecha_programada: datetime = Query(...), db: Session = Depends(get_database_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
    return service.obtener_por_fecha(db, fecha_programada)