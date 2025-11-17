from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from core.database_connection import get_database_session
from services.empleado.puesto_service import PuestoService
from schemas.empleado.puesto_schema import PuestoCreate, PuestoUpdate, PuestoResponse

security = HTTPBearer()
api_router = APIRouter(prefix="/puesto", tags=["Puesto"])

def get_puesto_service(db: Session = Depends(get_database_session)) -> PuestoService:
    """
    Dependency para obtener la instancia del servicio de Puesto
    """
    return PuestoService(db)

# Crear un puesto
@api_router.post("/", response_model=PuestoResponse,  status_code=status.HTTP_201_CREATED)
async def crear_puesto(
    puesto_data: PuestoCreate,
    service: PuestoService = Depends(get_puesto_service),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        return service.crear_puesto(puesto_data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# Obtener todos los puestos
@api_router.get("/", response_model=List[PuestoResponse])
def obtener_puestos(
    skip: int = 0,
    limit: int = 100,
    service: PuestoService = Depends(get_puesto_service),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        return service.obtener_todos_los_puestos(skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# Obtener puesto por ID
@api_router.get("/{puesto_id}", response_model=PuestoResponse)
def obtener_puesto(
    puesto_id: int,
    service: PuestoService = Depends(get_puesto_service),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    puesto = service.obtener_puesto_por_id(puesto_id)
    if not puesto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Puesto no encontrado")
    return puesto

# Actualizar puesto
@api_router.put("/{puesto_id}", response_model=PuestoResponse)
def actualizar_puesto(
    puesto_id: int,
    puesto_update: PuestoUpdate,
    service: PuestoService = Depends(get_puesto_service),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    puesto_actualizado = service.actualizar_puesto(puesto_id, puesto_update)
    if not puesto_actualizado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Puesto no encontrado")
    return puesto_actualizado

# Eliminar puesto (baja lógica)
@api_router.delete("/{puesto_id}")
def eliminar_puesto(
    puesto_id: int,
    service: PuestoService = Depends(get_puesto_service),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    eliminado = service.eliminar_puesto(puesto_id)
    if not eliminado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Puesto no encontrado")
    return {"detail": "Puesto eliminado correctamente"}
