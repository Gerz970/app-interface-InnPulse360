"""
Rutas API para gestión de asignación de roles a usuarios
Define los endpoints para operaciones de vinculación Usuario-Roles
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from core.database_connection import get_database_session
from services.seguridad.usuario_rol_service import UsuarioRolService
from services.seguridad.usuario_service import UsuarioService
from schemas.seguridad.usuario_rol_schemas import UsuarioRolAssign, UsuarioRolBulkAssign, RolSimpleResponse
from schemas.seguridad.usuario_response import UsuarioResponse

# Crear el router
router = APIRouter(
    prefix="/usuarios",
    tags=["Usuario-Roles"],
    responses={
        404: {"description": "Usuario o rol no encontrado"},
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


@router.post("/{usuario_id}/roles/{rol_id}", status_code=status.HTTP_201_CREATED)
async def assign_rol_to_usuario(
    usuario_id: int,
    rol_id: int,
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """
    Asignar un rol específico a un usuario
    
    - **usuario_id**: ID del usuario
    - **rol_id**: ID del rol a asignar
    """
    try:
        usuario_rol_service = UsuarioRolService(db)
        success = usuario_rol_service.assign_rol_to_usuario(usuario_id, rol_id)
        
        if success:
            return {"message": "Rol asignado exitosamente al usuario"}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se pudo asignar el rol"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.delete("/{usuario_id}/roles/{rol_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_rol_from_usuario(
    usuario_id: int,
    rol_id: int,
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """
    Remover un rol específico de un usuario
    
    - **usuario_id**: ID del usuario
    - **rol_id**: ID del rol a remover
    """
    try:
        usuario_rol_service = UsuarioRolService(db)
        success = usuario_rol_service.remove_rol_from_usuario(usuario_id, rol_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se pudo remover el rol"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.get("/{usuario_id}/roles", response_model=List[RolSimpleResponse])
async def get_usuario_roles(
    usuario_id: int,
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """
    Obtener todos los roles asignados a un usuario
    
    - **usuario_id**: ID del usuario
    """
    try:
        usuario_rol_service = UsuarioRolService(db)
        return usuario_rol_service.get_usuario_roles(usuario_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.put("/{usuario_id}/roles", response_model=dict)
async def bulk_assign_roles_to_usuario(
    usuario_id: int,
    roles_data: UsuarioRolBulkAssign,
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """
    Asignar múltiples roles a un usuario (solo los que no estén ya asignados)
    
    - **usuario_id**: ID del usuario
    - **roles_data**: Lista de IDs de roles a asignar
    """
    try:
        usuario_rol_service = UsuarioRolService(db)
        assigned_count = usuario_rol_service.bulk_assign_roles_to_usuario(
            usuario_id, roles_data.roles_ids
        )
        
        return {
            "message": f"Se asignaron {assigned_count} roles al usuario",
            "total_requested": len(roles_data.roles_ids),
            "assigned": assigned_count,
            "skipped": len(roles_data.roles_ids) - assigned_count
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.delete("/{usuario_id}/roles", response_model=dict)
async def bulk_remove_roles_from_usuario(
    usuario_id: int,
    roles_data: UsuarioRolBulkAssign,
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """
    Remover múltiples roles de un usuario
    
    - **usuario_id**: ID del usuario
    - **roles_data**: Lista de IDs de roles a remover
    """
    try:
        usuario_rol_service = UsuarioRolService(db)
        removed_count = usuario_rol_service.bulk_remove_roles_from_usuario(
            usuario_id, roles_data.roles_ids
        )
        
        return {
            "message": f"Se removieron {removed_count} roles del usuario",
            "total_requested": len(roles_data.roles_ids),
            "removed": removed_count,
            "not_found": len(roles_data.roles_ids) - removed_count
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.get("/{usuario_id}/with-roles", response_model=UsuarioResponse)
async def get_usuario_with_roles(
    usuario_id: int,
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """
    Obtener un usuario con todos sus roles
    
    - **usuario_id**: ID del usuario
    """
    try:
        usuario_rol_service = UsuarioRolService(db)
        return usuario_rol_service.get_usuario_with_roles(usuario_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


# Rutas para roles (obtener usuarios por rol)
@router.get("/by-rol/{rol_id}", response_model=List[UsuarioResponse])
async def get_usuarios_by_rol(
    rol_id: int,
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """
    Obtener todos los usuarios que tienen un rol específico
    
    - **rol_id**: ID del rol
    """
    try:
        usuario_rol_service = UsuarioRolService(db)
        return usuario_rol_service.get_rol_usuarios(rol_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )
