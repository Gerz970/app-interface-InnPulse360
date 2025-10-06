"""
Rutas API para País
Endpoints para operaciones CRUD de países
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from core.database_connection import get_database_session
from services.catalogos.pais_service import PaisService
from services.seguridad.usuario_service import UsuarioService
from schemas.catalogos.pais_schemas import PaisCreate, PaisUpdate, PaisResponse
from schemas.seguridad.usuario_response import UsuarioResponse

# Crear router para países
router = APIRouter(prefix="/paises", tags=["Países"])

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


@router.post("/", response_model=PaisResponse, status_code=status.HTTP_201_CREATED)
async def create_pais(
    pais_data: PaisCreate,
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """
    Crear un nuevo país
    
    - **nombre**: Nombre del país (requerido)
    - **id_estatus**: Estatus del país (1=Activo por defecto)
    """
    try:
        service = PaisService(db)
        return service.create_pais(pais_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear país: {str(e)}"
        )


@router.get("/", response_model=List[PaisResponse])
async def get_paises(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """
    Obtener lista de países activos con paginación
    
    - **skip**: Número de registros a saltar (por defecto: 0)
    - **limit**: Número máximo de registros a retornar (por defecto: 100, máximo: 1000)
    """
    try:
        service = PaisService(db)
        return service.get_all_paises(skip, limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener países: {str(e)}"
        )


@router.get("/{id_pais}", response_model=PaisResponse)
async def get_pais_by_id(
    id_pais: int,
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """
    Obtener un país por su ID
    
    - **id_pais**: ID único del país
    """
    try:
        service = PaisService(db)
        pais = service.get_pais_by_id(id_pais)
        if not pais:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="País no encontrado"
            )
        return pais
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener país: {str(e)}"
        )


@router.get("/nombre/{nombre}", response_model=PaisResponse)
async def get_pais_by_nombre(
    nombre: str,
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """
    Obtener un país por su nombre
    
    - **nombre**: Nombre del país
    """
    try:
        service = PaisService(db)
        pais = service.get_pais_by_nombre(nombre)
        if not pais:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="País no encontrado"
            )
        return pais
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener país: {str(e)}"
        )


@router.put("/{id_pais}", response_model=PaisResponse)
async def update_pais(
    id_pais: int,
    pais_data: PaisUpdate,
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """
    Actualizar un país existente
    
    - **id_pais**: ID único del país
    - **nombre**: Nuevo nombre del país (opcional)
    - **id_estatus**: Nuevo estatus del país (opcional)
    """
    try:
        service = PaisService(db)
        pais = service.update_pais(id_pais, pais_data)
        if not pais:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="País no encontrado"
            )
        return pais
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar país: {str(e)}"
        )


@router.delete("/{id_pais}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pais(
    id_pais: int,
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """
    Eliminar un país (eliminación lógica)
    
    - **id_pais**: ID único del país
    """
    try:
        service = PaisService(db)
        success = service.delete_pais(id_pais)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="País no encontrado"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar país: {str(e)}"
        )


@router.patch("/{id_pais}/reactivate", status_code=status.HTTP_200_OK)
async def reactivate_pais(
    id_pais: int,
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """
    Reactivar un país (cambiar estatus a activo)
    
    - **id_pais**: ID único del país
    """
    try:
        service = PaisService(db)
        success = service.reactivate_pais(id_pais)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="País no encontrado"
            )
        return {"message": "País reactivado exitosamente"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al reactivar país: {str(e)}"
        )
