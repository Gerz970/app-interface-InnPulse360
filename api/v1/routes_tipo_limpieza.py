from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database_connection import get_database_session
from schemas.camarista.tipos_limpieza_schema import TipoLimpiezaCreate, TipoLimpiezaUpdate
from services.camarista.tipo_limpieza_service import TipoLimpiezaService
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter(
    prefix="/tipos-limpieza",
    tags=["Tipos de limpieza"]
)

service = TipoLimpiezaService()
security = HTTPBearer()

# 🔹 Obtener todos los tipos de limpieza
@router.get("/")
def obtener_todos(db: Session = Depends(get_database_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
    tipos = service.obtener_todos(db)
    return tipos


# 🔹 Obtener un tipo de limpieza por ID
@router.get("/{id_tipo_limpieza}")
def obtener_por_id(id_tipo_limpieza: int, db: Session = Depends(get_database_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
    tipo = service.obtener_por_id(db, id_tipo_limpieza)
    if not tipo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tipo de limpieza no encontrado"
        )
    return tipo


# 🔹 Crear un nuevo tipo de limpieza
@router.post("/", status_code=status.HTTP_201_CREATED)
def crear_tipo_limpieza(data: TipoLimpiezaCreate, db: Session = Depends(get_database_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
    nuevo_tipo = service.crear(db, data)
    return {"mensaje": "Tipo de limpieza creado correctamente", "data": nuevo_tipo}


# 🔹 Actualizar un tipo de limpieza existente
@router.put("/{id_tipo_limpieza}")
def actualizar_tipo_limpieza(id_tipo_limpieza: int, data: TipoLimpiezaUpdate, db: Session = Depends(get_database_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
    tipo_actualizado = service.actualizar(db, id_tipo_limpieza, data)
    if not tipo_actualizado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tipo de limpieza no encontrado"
        )
    return {"mensaje": "Tipo de limpieza actualizado correctamente", "data": tipo_actualizado}


# 🔹 Eliminar un tipo de limpieza
@router.delete("/{id_tipo_limpieza}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_tipo_limpieza(id_tipo_limpieza: int, db: Session = Depends(get_database_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
    eliminado = service.eliminar(db, id_tipo_limpieza)
    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tipo de limpieza no encontrado"
        )
    return {"mensaje": "Tipo de limpieza eliminado correctamente"}
