"""
Rutas API para asignación de características a tipos de habitación
Endpoints para gestionar la relación TipoHabitacion-Caracteristica
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from core.database_connection import get_database_session
from services.hotel.tipo_habitacion_caracteristica_service import TipoHabitacionCaracteristicaService
from services.seguridad.usuario_service import UsuarioService
from schemas.hotel.tipo_habitacion_caracteristica_schemas import (
    TipoHabitacionCaracteristicaBulkAssign
)
from schemas.hotel.tipo_habitacion_schemas import TipoHabitacionResponse
from schemas.hotel.caracteristica_schemas import CaracteristicaResponse
from schemas.seguridad.usuario_response import UsuarioResponse

# Crear router para asignación de características
router = APIRouter(prefix="/tipos-habitacion", tags=["Asignación de Características"])

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


@router.post("/{tipo_habitacion_id}/caracteristicas/{caracteristica_id}", status_code=status.HTTP_201_CREATED)
async def assign_caracteristica_to_tipo_habitacion(
    tipo_habitacion_id: int,
    caracteristica_id: int,
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """
    Asignar una característica a un tipo de habitación
    
    - **tipo_habitacion_id**: ID del tipo de habitación
    - **caracteristica_id**: ID de la característica
    """
    try:
        service = TipoHabitacionCaracteristicaService(db)
        success = service.assign_caracteristica_to_tipo_habitacion(tipo_habitacion_id, caracteristica_id)
        if success:
            return {"message": "Característica asignada exitosamente al tipo de habitación"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al asignar característica: {str(e)}"
        )


@router.delete("/{tipo_habitacion_id}/caracteristicas/{caracteristica_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_caracteristica_from_tipo_habitacion(
    tipo_habitacion_id: int,
    caracteristica_id: int,
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """
    Remover una característica de un tipo de habitación
    
    - **tipo_habitacion_id**: ID del tipo de habitación
    - **caracteristica_id**: ID de la característica
    """
    try:
        service = TipoHabitacionCaracteristicaService(db)
        success = service.remove_caracteristica_from_tipo_habitacion(tipo_habitacion_id, caracteristica_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Asignación no encontrada"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al remover característica: {str(e)}"
        )


@router.get("/{tipo_habitacion_id}/caracteristicas", response_model=List[CaracteristicaResponse])
async def get_caracteristicas_by_tipo_habitacion(
    tipo_habitacion_id: int,
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """
    Obtener las características de un tipo de habitación
    
    - **tipo_habitacion_id**: ID del tipo de habitación
    """
    try:
        service = TipoHabitacionCaracteristicaService(db)
        return service.get_caracteristicas_by_tipo_habitacion(tipo_habitacion_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener características: {str(e)}"
        )


@router.put("/{tipo_habitacion_id}/caracteristicas", status_code=status.HTTP_200_OK)
async def bulk_assign_caracteristicas_to_tipo_habitacion(
    tipo_habitacion_id: int,
    caracteristicas_data: TipoHabitacionCaracteristicaBulkAssign,
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """
    Asignar múltiples características a un tipo de habitación
    
    - **tipo_habitacion_id**: ID del tipo de habitación
    - **caracteristicas_ids**: Lista de IDs de características a asignar
    """
    try:
        service = TipoHabitacionCaracteristicaService(db)
        assigned_count = service.bulk_assign_caracteristicas_to_tipo_habitacion(
            tipo_habitacion_id, caracteristicas_data.caracteristicas_ids
        )
        return {
            "message": f"Se asignaron {assigned_count} características exitosamente",
            "assigned_count": assigned_count,
            "total_requested": len(caracteristicas_data.caracteristicas_ids)
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al asignar características: {str(e)}"
        )


@router.delete("/{tipo_habitacion_id}/caracteristicas", status_code=status.HTTP_200_OK)
async def bulk_remove_caracteristicas_from_tipo_habitacion(
    tipo_habitacion_id: int,
    caracteristicas_data: TipoHabitacionCaracteristicaBulkAssign,
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """
    Remover múltiples características de un tipo de habitación
    
    - **tipo_habitacion_id**: ID del tipo de habitación
    - **caracteristicas_ids**: Lista de IDs de características a remover
    """
    try:
        service = TipoHabitacionCaracteristicaService(db)
        removed_count = service.bulk_remove_caracteristicas_from_tipo_habitacion(
            tipo_habitacion_id, caracteristicas_data.caracteristicas_ids
        )
        return {
            "message": f"Se removieron {removed_count} características exitosamente",
            "removed_count": removed_count,
            "total_requested": len(caracteristicas_data.caracteristicas_ids)
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al remover características: {str(e)}"
        )


@router.get("/caracteristicas/{caracteristica_id}/tipos-habitacion", response_model=List[TipoHabitacionResponse])
async def get_tipos_habitacion_by_caracteristica(
    caracteristica_id: int,
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """
    Obtener los tipos de habitación que tienen una característica específica
    
    - **caracteristica_id**: ID de la característica
    """
    try:
        service = TipoHabitacionCaracteristicaService(db)
        return service.get_tipos_habitacion_by_caracteristica(caracteristica_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener tipos de habitación: {str(e)}"
        )
