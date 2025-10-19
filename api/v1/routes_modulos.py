"""
Rutas API para gestión de módulos
Incluye CRUD completo y gestión de asociaciones con roles
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from core.config import Settings
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from core.database_connection import get_database_session
from services.seguridad.modulos_service import ModulosService
from schemas.seguridad.modulos_create import ModulosCreate
from schemas.seguridad.modulos_update import ModulosUpdate
from schemas.seguridad.modulos_response import ModulosResponse
from schemas.seguridad.modulo_rol_schemas import (
    ModuloRolAsignacion, 
    ModuloRolAsignacionMultiple, 
    ModuloRolResponse
)

# Crear instancia de settings
settings = Settings()

# Configurar seguridad
security = HTTPBearer()


# Configurar router
router = APIRouter(
    prefix="/modulos",
    tags=["módulos"],
    responses={404: {"description": "Not found"}},
)


def get_modulos_service(
    db: Session = Depends(get_database_session)
) -> ModulosService:
    """
    Dependency para obtener el servicio de módulos
    
    Args:
        db (Session): Sesión de base de datos
        
    Returns:
        ModulosService: Instancia del servicio
    """
    return ModulosService(db)


# ==================== CRUD DE MÓDULOS ====================

@router.post("/", response_model=ModulosResponse, status_code=status.HTTP_201_CREATED)
def crear_modulo(
    modulo_data: ModulosCreate,
    modulo_service: ModulosService = Depends(get_modulos_service),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Crear un nuevo módulo
    
    - **nombre**: Nombre del módulo (máximo 25 caracteres)
    - **descripcion**: Descripción del módulo (opcional, máximo 100 caracteres)
    - **icono**: Icono del módulo (opcional, máximo 25 caracteres)
    - **ruta**: Ruta del módulo (opcional, máximo 250 caracteres)
    - **id_estatus**: Estatus del módulo (1=Activo, 0=Inactivo)
    """
    return modulo_service.create_modulo(modulo_data)


@router.get("/", response_model=List[ModulosResponse])
def obtener_modulos(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    activos_only: bool = Query(False, description="Solo obtener módulos activos"),
    modulo_service: ModulosService = Depends(get_modulos_service),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Obtener todos los módulos con paginación
    
    - **skip**: Número de registros a omitir (paginación)
    - **limit**: Número máximo de registros a retornar
    - **activos_only**: Si solo obtener módulos activos
    """
    return modulo_service.get_all_modulos(skip, limit, activos_only)


@router.get("/{id_modulo}", response_model=ModulosResponse)
def obtener_modulo_por_id(
    id_modulo: int,
    modulo_service: ModulosService = Depends(get_modulos_service),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Obtener un módulo por su ID
    
    - **id_modulo**: ID único del módulo
    """
    return modulo_service.get_modulo_by_id(id_modulo)


@router.put("/{id_modulo}", response_model=ModulosResponse)
def actualizar_modulo(
    id_modulo: int,
    modulo_data: ModulosUpdate,
    modulo_service: ModulosService = Depends(get_modulos_service),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Actualizar un módulo existente
    
    - **id_modulo**: ID del módulo a actualizar
    - Todos los campos son opcionales para permitir actualizaciones parciales
    """
    return modulo_service.update_modulo(id_modulo, modulo_data)


@router.delete("/{id_modulo}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_modulo(
    id_modulo: int,
    modulo_service: ModulosService = Depends(get_modulos_service),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Eliminar un módulo (soft delete)
    
    - **id_modulo**: ID del módulo a eliminar
    """
    modulo_service.delete_modulo(id_modulo)
    return {"message": "Módulo eliminado correctamente"}


# ==================== ASOCIACIONES MÓDULO-ROL ====================

@router.post("/asignar-rol", status_code=status.HTTP_200_OK)
def asignar_modulo_a_rol(
    asignacion: ModuloRolAsignacion,
    modulo_service: ModulosService = Depends(get_modulos_service),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Asignar un módulo a un rol
    
    - **modulo_id**: ID del módulo a asignar
    - **rol_id**: ID del rol al que se asigna el módulo
    """
    modulo_service.asignar_modulo_a_rol(asignacion.modulo_id, asignacion.rol_id)
    return {"message": "Módulo asignado al rol correctamente"}


@router.delete("/desasignar-rol", status_code=status.HTTP_200_OK)
def desasignar_modulo_de_rol(
    modulo_id: int = Query(..., description="ID del módulo"),
    rol_id: int = Query(..., description="ID del rol"),
    modulo_service: ModulosService = Depends(get_modulos_service),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Desasignar un módulo de un rol
    
    - **modulo_id**: ID del módulo a desasignar
    - **rol_id**: ID del rol del que se desasigna el módulo
    """
    modulo_service.desasignar_modulo_de_rol(modulo_id, rol_id)
    return {"message": "Módulo desasignado del rol correctamente"}


@router.post("/asignar-multiples", status_code=status.HTTP_200_OK)
def asignar_multiples_modulos_a_rol(
    asignacion: ModuloRolAsignacionMultiple,
    modulo_service: ModulosService = Depends(get_modulos_service),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Asignar múltiples módulos a un rol
    
    - **rol_id**: ID del rol al que se asignan los módulos
    - **modulos_ids**: Lista de IDs de módulos a asignar
    """
    modulo_service.asignar_multiples_modulos_a_rol(asignacion.rol_id, asignacion.modulos_ids)
    return {"message": "Módulos asignados al rol correctamente"}


@router.get("/por-rol/{rol_id}", response_model=List[ModulosResponse])
def obtener_modulos_por_rol(
    rol_id: int,
    modulo_service: ModulosService = Depends(get_modulos_service),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Obtener todos los módulos asignados a un rol
    
    - **rol_id**: ID del rol
    """
    return modulo_service.get_modulos_por_rol(rol_id)


# ==================== ENDPOINTS ADICIONALES ====================

@router.get("/buscar/nombre/{nombre}", response_model=Optional[ModulosResponse])
def buscar_modulo_por_nombre(
    nombre: str,
    modulo_service: ModulosService = Depends(get_modulos_service),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Buscar un módulo por su nombre
    
    - **nombre**: Nombre del módulo a buscar
    """
    try:
        from dao.seguridad.dao_modulos import ModulosDAO
        dao = ModulosDAO(modulo_service.db)
        modulo = dao.get_by_nombre(nombre)
        
        if not modulo:
            return None
            
        return modulo_service._modulo_to_response(modulo)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar módulo por nombre: {str(e)}"
        )


@router.get("/activos/", response_model=List[ModulosResponse])
def obtener_modulos_activos(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    modulo_service: ModulosService = Depends(get_modulos_service),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Obtener solo los módulos activos
    
    - **skip**: Número de registros a omitir (paginación)
    - **limit**: Número máximo de registros a retornar
    """
    return modulo_service.get_all_modulos(skip, limit, activos_only=True)
