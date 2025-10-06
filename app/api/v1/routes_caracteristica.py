"""
Rutas API para Caracteristica
Endpoints para operaciones CRUD de características
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from core.database_connection import get_database_session
from services.caracteristica_service import CaracteristicaService
from services.usuario_service import UsuarioService
from schemas.hotel.caracteristica_schemas import CaracteristicaCreate, CaracteristicaUpdate, CaracteristicaResponse
from schemas.seguridad.usuario_response import UsuarioResponse

# Crear router para características
router = APIRouter(prefix="/caracteristicas", tags=["Características"])

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


@router.post("/", response_model=CaracteristicaResponse, status_code=status.HTTP_201_CREATED)
async def create_caracteristica(
    caracteristica_data: CaracteristicaCreate,
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """
    Crear una nueva característica
    
    - **caracteristica**: Nombre de la característica (requerido)
    - **descripcion**: Descripción de la característica (opcional)
    """
    try:
        service = CaracteristicaService(db)
        return service.create_caracteristica(caracteristica_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear característica: {str(e)}"
        )


@router.get("/", response_model=List[CaracteristicaResponse])
async def get_caracteristicas(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """
    Obtener lista de características con paginación
    
    - **skip**: Número de registros a saltar (por defecto: 0)
    - **limit**: Número máximo de registros a retornar (por defecto: 100, máximo: 1000)
    """
    try:
        service = CaracteristicaService(db)
        return service.get_all_caracteristicas(skip, limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener características: {str(e)}"
        )


@router.get("/{id_caracteristica}", response_model=CaracteristicaResponse)
async def get_caracteristica_by_id(
    id_caracteristica: int,
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """
    Obtener una característica por su ID
    
    - **id_caracteristica**: ID único de la característica
    """
    try:
        service = CaracteristicaService(db)
        caracteristica = service.get_caracteristica_by_id(id_caracteristica)
        if not caracteristica:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Característica no encontrada"
            )
        return caracteristica
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener característica: {str(e)}"
        )


@router.get("/nombre/{caracteristica}", response_model=CaracteristicaResponse)
async def get_caracteristica_by_nombre(
    caracteristica: str,
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """
    Obtener una característica por su nombre
    
    - **caracteristica**: Nombre de la característica
    """
    try:
        service = CaracteristicaService(db)
        caracteristica_obj = service.get_caracteristica_by_nombre(caracteristica)
        if not caracteristica_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Característica no encontrada"
            )
        return caracteristica_obj
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener característica: {str(e)}"
        )


@router.put("/{id_caracteristica}", response_model=CaracteristicaResponse)
async def update_caracteristica(
    id_caracteristica: int,
    caracteristica_data: CaracteristicaUpdate,
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """
    Actualizar una característica existente
    
    - **id_caracteristica**: ID único de la característica
    - **caracteristica**: Nuevo nombre de la característica (opcional)
    - **descripcion**: Nueva descripción de la característica (opcional)
    """
    try:
        service = CaracteristicaService(db)
        caracteristica = service.update_caracteristica(id_caracteristica, caracteristica_data)
        if not caracteristica:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Característica no encontrada"
            )
        return caracteristica
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar característica: {str(e)}"
        )


@router.delete("/{id_caracteristica}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_caracteristica(
    id_caracteristica: int,
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """
    Eliminar una característica
    
    - **id_caracteristica**: ID único de la característica
    """
    try:
        service = CaracteristicaService(db)
        success = service.delete_caracteristica(id_caracteristica)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Característica no encontrada"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar característica: {str(e)}"
        )
