"""
Rutas API para Estado
Endpoints para operaciones CRUD de estados
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from core.database_connection import get_database_session
from services.catalogos.estado_service import EstadoService
from services.seguridad.usuario_service import UsuarioService
from schemas.catalogos.estado_schemas import EstadoCreate, EstadoUpdate, EstadoResponse
from schemas.seguridad.usuario_response import UsuarioResponse

# Crear router para estados
router = APIRouter(prefix="/estados", tags=["Estados"])

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


@router.post("/", response_model=EstadoResponse, status_code=status.HTTP_201_CREATED)
async def create_estado(
    estado_data: EstadoCreate,
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """
    Crear un nuevo estado
    
    - **id_pais**: ID del país al que pertenece el estado (requerido)
    - **nombre**: Nombre del estado (requerido)
    - **id_estatus**: Estatus del estado (1=Activo por defecto)
    """
    try:
        service = EstadoService(db)
        return service.create_estado(estado_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear estado: {str(e)}"
        )


@router.get("/", response_model=List[EstadoResponse])
async def get_estados(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """
    Obtener lista de estados activos con paginación
    
    - **skip**: Número de registros a saltar (por defecto: 0)
    - **limit**: Número máximo de registros a retornar (por defecto: 100, máximo: 1000)
    """
    try:
        service = EstadoService(db)
        return service.get_all_estados(skip, limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener estados: {str(e)}"
        )


@router.get("/pais/{id_pais}", response_model=List[EstadoResponse])
async def get_estados_by_pais(
    id_pais: int,
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """
    Obtener todos los estados de un país específico
    
    - **id_pais**: ID del país
    """
    try:
        service = EstadoService(db)
        return service.get_estados_by_pais(id_pais)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener estados del país: {str(e)}"
        )


@router.get("/{id_estado}", response_model=EstadoResponse)
async def get_estado_by_id(
    id_estado: int,
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """
    Obtener un estado por su ID
    
    - **id_estado**: ID único del estado
    """
    try:
        service = EstadoService(db)
        estado = service.get_estado_by_id(id_estado)
        if not estado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Estado no encontrado"
            )
        return estado
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener estado: {str(e)}"
        )


@router.get("/nombre/{nombre}", response_model=EstadoResponse)
async def get_estado_by_nombre(
    nombre: str,
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """
    Obtener un estado por su nombre
    
    - **nombre**: Nombre del estado
    """
    try:
        service = EstadoService(db)
        estado = service.get_estado_by_nombre(nombre)
        if not estado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Estado no encontrado"
            )
        return estado
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener estado: {str(e)}"
        )


@router.put("/{id_estado}", response_model=EstadoResponse)
async def update_estado(
    id_estado: int,
    estado_data: EstadoUpdate,
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """
    Actualizar un estado existente
    
    - **id_estado**: ID único del estado
    - **id_pais**: ID del país (opcional)
    - **nombre**: Nuevo nombre del estado (opcional)
    - **id_estatus**: Nuevo estatus del estado (opcional)
    """
    try:
        service = EstadoService(db)
        estado = service.update_estado(id_estado, estado_data)
        if not estado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Estado no encontrado"
            )
        return estado
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar estado: {str(e)}"
        )


@router.delete("/{id_estado}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_estado(
    id_estado: int,
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """
    Eliminar un estado (eliminación lógica)
    
    - **id_estado**: ID único del estado
    """
    try:
        service = EstadoService(db)
        success = service.delete_estado(id_estado)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Estado no encontrado"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar estado: {str(e)}"
        )


@router.patch("/{id_estado}/reactivate", status_code=status.HTTP_200_OK)
async def reactivate_estado(
    id_estado: int,
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """
    Reactivar un estado (cambiar estatus a activo)
    
    - **id_estado**: ID único del estado
    """
    try:
        service = EstadoService(db)
        success = service.reactivate_estado(id_estado)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Estado no encontrado"
            )
        return {"message": "Estado reactivado exitosamente"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al reactivar estado: {str(e)}"
        )
