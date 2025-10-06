"""
Rutas API para gestión de Roles
Define los endpoints para operaciones CRUD de roles
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from core.database_connection import get_database_session
from services.roles_service import RolesService
from services.usuario_service import UsuarioService
from schemas.seguridad.roles_create import RolesCreate
from schemas.seguridad.roles_update import RolesUpdate
from schemas.seguridad.roles_response import RolesResponse
from schemas.seguridad.usuario_response import UsuarioResponse

# Crear el router
router = APIRouter(
    prefix="/roles",
    tags=["Roles"],
    responses={
        404: {"description": "Rol no encontrado"},
        400: {"description": "Datos inválidos"},
        500: {"description": "Error interno del servidor"}
    }
)

# Configurar seguridad
security = HTTPBearer()


def get_usuario_service(
    db: Session = Depends(get_database_session)
) -> UsuarioService:
    """
    Dependency para obtener el servicio de usuario
    
    Args:
        db (Session): Sesión de base de datos
        
    Returns:
        UsuarioService: Instancia del servicio
    """
    return UsuarioService(db)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    usuario_service: UsuarioService = Depends(get_usuario_service)
) -> UsuarioResponse:
    """
    Dependency para obtener el usuario actual desde el token JWT
    
    Args:
        credentials (HTTPAuthorizationCredentials): Credenciales del token
        usuario_service (UsuarioService): Servicio de usuario
        
    Returns:
        UsuarioResponse: Usuario actual
        
    Raises:
        HTTPException: Si el token es inválido
    """
    return usuario_service.get_current_user(credentials.credentials)


@router.post("/", response_model=RolesResponse, status_code=status.HTTP_201_CREATED)
async def create_rol(
    roles_data: RolesCreate,
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """
    Crear un nuevo rol
    
    - **rol**: Nombre del rol (único)
    - **descripcion**: Descripción del rol
    - **estatus_id**: Estatus del rol (1=Activo por defecto)
    """
    try:
        roles_service = RolesService(db)
        return roles_service.create_rol(roles_data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.get("/", response_model=List[RolesResponse])
async def get_all_roles(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """
    Obtener lista de roles activos
    
    - **skip**: Número de registros a saltar (paginación)
    - **limit**: Número máximo de registros a retornar (máximo 1000)
    """
    try:
        roles_service = RolesService(db)
        return roles_service.get_all_roles(skip, limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.get("/{id_rol}", response_model=RolesResponse)
async def get_rol_by_id(
    id_rol: int,
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """
    Obtener un rol por ID
    
    - **id_rol**: ID único del rol
    """
    try:
        roles_service = RolesService(db)
        rol = roles_service.get_rol_by_id(id_rol)
        if not rol:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rol no encontrado"
            )
        return rol
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.get("/by-name/{rol}", response_model=RolesResponse)
async def get_rol_by_name(
    rol: str,
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """
    Obtener un rol por nombre
    
    - **rol**: Nombre del rol
    """
    try:
        roles_service = RolesService(db)
        rol_found = roles_service.get_rol_by_name(rol)
        if not rol_found:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rol no encontrado"
            )
        return rol_found
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.put("/{id_rol}", response_model=RolesResponse)
async def update_rol(
    id_rol: int,
    roles_data: RolesUpdate,
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """
    Actualizar un rol existente
    
    - **id_rol**: ID único del rol a actualizar
    - **roles_data**: Datos actualizados del rol (todos los campos son opcionales)
    """
    try:
        roles_service = RolesService(db)
        updated_rol = roles_service.update_rol(id_rol, roles_data)
        if not updated_rol:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rol no encontrado"
            )
        return updated_rol
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.delete("/{id_rol}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_rol(
    id_rol: int,
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """
    Eliminar un rol (eliminación lógica - cambia estatus a inactivo)
    
    - **id_rol**: ID único del rol a eliminar
    """
    try:
        roles_service = RolesService(db)
        success = roles_service.delete_rol(id_rol)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rol no encontrado"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.patch("/{id_rol}/reactivate", response_model=RolesResponse)
async def reactivate_rol(
    id_rol: int,
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """
    Reactivar un rol (cambia estatus a activo)
    
    - **id_rol**: ID único del rol a reactivar
    """
    try:
        roles_service = RolesService(db)
        success = roles_service.reactivate_rol(id_rol)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rol no encontrado"
            )
        
        # Retornar el rol reactivado
        reactivated_rol = roles_service.get_rol_by_id(id_rol)
        return reactivated_rol
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )
