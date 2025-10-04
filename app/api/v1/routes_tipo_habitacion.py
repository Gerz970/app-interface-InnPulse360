"""
Rutas API para TipoHabitacion
Endpoints para operaciones CRUD de tipos de habitación
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from core.database_connection import get_database_session
from services.tipo_habitacion_service import TipoHabitacionService
from schemas.catalogos.tipo_habitacion_schemas import TipoHabitacionCreate, TipoHabitacionUpdate, TipoHabitacionResponse

# Crear router para tipos de habitación
router = APIRouter(prefix="/tipos-habitacion", tags=["Tipos de Habitación"])


@router.post("/", response_model=TipoHabitacionResponse, status_code=status.HTTP_201_CREATED)
async def create_tipo_habitacion(
    tipo_habitacion_data: TipoHabitacionCreate,
    db: Session = Depends(get_database_session)
):
    """
    Crear un nuevo tipo de habitación
    
    - **clave**: Clave del tipo de habitación (opcional)
    - **tipo_habitacion**: Nombre del tipo de habitación (requerido)
    - **estatus_id**: Estatus del tipo de habitación (1=Activo por defecto)
    """
    try:
        service = TipoHabitacionService(db)
        return service.create_tipo_habitacion(tipo_habitacion_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear tipo de habitación: {str(e)}"
        )


@router.get("/", response_model=List[TipoHabitacionResponse])
async def get_tipos_habitacion(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    db: Session = Depends(get_database_session)
):
    """
    Obtener lista de tipos de habitación activos con paginación
    
    - **skip**: Número de registros a saltar (por defecto: 0)
    - **limit**: Número máximo de registros a retornar (por defecto: 100, máximo: 1000)
    """
    try:
        service = TipoHabitacionService(db)
        return service.get_all_tipos_habitacion(skip, limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener tipos de habitación: {str(e)}"
        )


@router.get("/{id_tipoHabitacion}", response_model=TipoHabitacionResponse)
async def get_tipo_habitacion_by_id(
    id_tipoHabitacion: int,
    db: Session = Depends(get_database_session)
):
    """
    Obtener un tipo de habitación por su ID
    
    - **id_tipoHabitacion**: ID único del tipo de habitación
    """
    try:
        service = TipoHabitacionService(db)
        tipo_habitacion = service.get_tipo_habitacion_by_id(id_tipoHabitacion)
        if not tipo_habitacion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tipo de habitación no encontrado"
            )
        return tipo_habitacion
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener tipo de habitación: {str(e)}"
        )


@router.get("/clave/{clave}", response_model=TipoHabitacionResponse)
async def get_tipo_habitacion_by_clave(
    clave: str,
    db: Session = Depends(get_database_session)
):
    """
    Obtener un tipo de habitación por su clave
    
    - **clave**: Clave del tipo de habitación
    """
    try:
        service = TipoHabitacionService(db)
        tipo_habitacion = service.get_tipo_habitacion_by_clave(clave)
        if not tipo_habitacion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tipo de habitación no encontrado"
            )
        return tipo_habitacion
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener tipo de habitación: {str(e)}"
        )


@router.get("/nombre/{tipo_habitacion}", response_model=TipoHabitacionResponse)
async def get_tipo_habitacion_by_nombre(
    tipo_habitacion: str,
    db: Session = Depends(get_database_session)
):
    """
    Obtener un tipo de habitación por su nombre
    
    - **tipo_habitacion**: Nombre del tipo de habitación
    """
    try:
        service = TipoHabitacionService(db)
        tipo_habitacion_obj = service.get_tipo_habitacion_by_nombre(tipo_habitacion)
        if not tipo_habitacion_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tipo de habitación no encontrado"
            )
        return tipo_habitacion_obj
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener tipo de habitación: {str(e)}"
        )


@router.put("/{id_tipoHabitacion}", response_model=TipoHabitacionResponse)
async def update_tipo_habitacion(
    id_tipoHabitacion: int,
    tipo_habitacion_data: TipoHabitacionUpdate,
    db: Session = Depends(get_database_session)
):
    """
    Actualizar un tipo de habitación existente
    
    - **id_tipoHabitacion**: ID único del tipo de habitación
    - **clave**: Nueva clave del tipo de habitación (opcional)
    - **tipo_habitacion**: Nuevo nombre del tipo de habitación (opcional)
    - **estatus_id**: Nuevo estatus del tipo de habitación (opcional)
    """
    try:
        service = TipoHabitacionService(db)
        tipo_habitacion = service.update_tipo_habitacion(id_tipoHabitacion, tipo_habitacion_data)
        if not tipo_habitacion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tipo de habitación no encontrado"
            )
        return tipo_habitacion
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar tipo de habitación: {str(e)}"
        )


@router.delete("/{id_tipoHabitacion}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tipo_habitacion(
    id_tipoHabitacion: int,
    db: Session = Depends(get_database_session)
):
    """
    Eliminar un tipo de habitación (eliminación lógica)
    
    - **id_tipoHabitacion**: ID único del tipo de habitación
    """
    try:
        service = TipoHabitacionService(db)
        success = service.delete_tipo_habitacion(id_tipoHabitacion)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tipo de habitación no encontrado"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar tipo de habitación: {str(e)}"
        )


@router.patch("/{id_tipoHabitacion}/reactivate", status_code=status.HTTP_200_OK)
async def reactivate_tipo_habitacion(
    id_tipoHabitacion: int,
    db: Session = Depends(get_database_session)
):
    """
    Reactivar un tipo de habitación (cambiar estatus a activo)
    
    - **id_tipoHabitacion**: ID único del tipo de habitación
    """
    try:
        service = TipoHabitacionService(db)
        success = service.reactivate_tipo_habitacion(id_tipoHabitacion)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tipo de habitación no encontrado"
            )
        return {"message": "Tipo de habitación reactivado exitosamente"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al reactivar tipo de habitación: {str(e)}"
        )
