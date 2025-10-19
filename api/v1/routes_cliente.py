"""
Rutas API para gestión de clientes
Define los endpoints para operaciones CRUD de clientes
Incluye validación de RFC único
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from core.database_connection import get_database_session
from services.cliente.cliente_service import ClienteService
from services.seguridad.usuario_service import UsuarioService
from schemas.cliente.cliente_create import ClienteCreate
from schemas.cliente.cliente_update import ClienteUpdate
from schemas.cliente.cliente_response import ClienteResponse
from schemas.seguridad.usuario_response import UsuarioResponse

# Crear el router
router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"],
    responses={
        404: {"description": "Cliente no encontrado"},
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


@router.post("/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
async def create_cliente(
    cliente_data: ClienteCreate,
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """
    Crear un nuevo cliente
    
    ⚠️ **VALIDACIÓN IMPORTANTE**: El RFC debe ser único. Si ya existe, retorna error 400.
    
    - **tipo_persona**: 1=Física, 2=Moral
    - **documento_identificacion**: Número de identificación
    - **nombre_razon_social**: Nombre completo o Razón Social
    - **rfc**: RFC (12-13 caracteres, único, validado)
    - **curp**: CURP (18 caracteres, validado)
    - **pais_id**: ID del país
    - **estado_id**: ID del estado
    - **correo_electronico**: Email del cliente
    - **representante**: Nombre del representante
    - **id_estatus**: Estatus (1=Activo, 0=Inactivo)
    """
    try:
        cliente_service = ClienteService(db)
        return cliente_service.crear_cliente(cliente_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.get("/", response_model=List[ClienteResponse])
async def get_all_clientes(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """
    Obtener todos los clientes con paginación
    
    - **skip**: Número de registros a saltar (paginación)
    - **limit**: Número máximo de registros a retornar
    """
    try:
        cliente_service = ClienteService(db)
        return cliente_service.obtener_todos_los_clientes(skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener clientes: {str(e)}"
        )


@router.get("/activos", response_model=List[ClienteResponse])
async def get_clientes_activos(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """
    Obtener solo los clientes activos
    
    - **skip**: Número de registros a saltar
    - **limit**: Número máximo de registros
    """
    try:
        cliente_service = ClienteService(db)
        return cliente_service.obtener_clientes_activos(skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener clientes activos: {str(e)}"
        )


@router.get("/{cliente_id}", response_model=ClienteResponse)
async def get_cliente(
    cliente_id: int,
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """
    Obtener un cliente por su ID
    
    - **cliente_id**: ID único del cliente
    """
    try:
        cliente_service = ClienteService(db)
        cliente = cliente_service.obtener_cliente_por_id(cliente_id)
        
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente con ID {cliente_id} no encontrado"
            )
        
        return cliente
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener cliente: {str(e)}"
        )


@router.put("/{cliente_id}", response_model=ClienteResponse)
async def update_cliente(
    cliente_id: int,
    cliente_data: ClienteUpdate,
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """
    Actualizar un cliente existente
    
    ⚠️ **VALIDACIÓN IMPORTANTE**: Si se actualiza el RFC, se valida que no exista duplicado.
    
    - **cliente_id**: ID del cliente a actualizar
    - Todos los campos son opcionales para permitir actualizaciones parciales
    """
    try:
        cliente_service = ClienteService(db)
        cliente = cliente_service.actualizar_cliente(cliente_id, cliente_data)
        
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente con ID {cliente_id} no encontrado"
            )
        
        return cliente
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar cliente: {str(e)}"
        )


@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cliente(
    cliente_id: int,
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """
    Eliminar un cliente (soft delete)
    
    - **cliente_id**: ID del cliente a eliminar
    """
    try:
        cliente_service = ClienteService(db)
        success = cliente_service.eliminar_cliente(cliente_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente con ID {cliente_id} no encontrado"
            )
        
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar cliente: {str(e)}"
        )


@router.get("/buscar/rfc/{rfc}", response_model=ClienteResponse)
async def buscar_cliente_por_rfc(
    rfc: str,
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """
    Buscar un cliente por su RFC
    
    - **rfc**: RFC del cliente a buscar
    """
    try:
        cliente_service = ClienteService(db)
        cliente = cliente_service.buscar_cliente_por_rfc(rfc)
        
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró cliente con RFC '{rfc}'"
            )
        
        return cliente
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar cliente por RFC: {str(e)}"
        )


@router.get("/verificar-rfc/{rfc}")
async def verificar_rfc_disponible(
    rfc: str,
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """
    Verificar si un RFC está disponible (no existe en la base de datos)
    
    - **rfc**: RFC a verificar
    
    Retorna:
    - **disponible**: True si el RFC está disponible, False si ya existe
    - **mensaje**: Mensaje descriptivo
    """
    try:
        from dao.cliente.dao_cliente import ClienteDAO
        dao = ClienteDAO(db)
        existe = dao.exists_by_rfc(rfc)
        
        return {
            "rfc": rfc.upper(),
            "disponible": not existe,
            "mensaje": "RFC disponible" if not existe else f"Ya existe un cliente registrado con el RFC '{rfc.upper()}'"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al verificar RFC: {str(e)}"
        )


@router.get("/buscar/nombre", response_model=List[ClienteResponse])
async def buscar_clientes_por_nombre(
    nombre: str = Query(..., min_length=1, description="Nombre o razón social a buscar"),
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """
    Buscar clientes por nombre o razón social (búsqueda parcial)
    
    - **nombre**: Texto a buscar en nombre/razón social
    - **skip**: Número de registros a saltar
    - **limit**: Número máximo de registros
    """
    try:
        cliente_service = ClienteService(db)
        return cliente_service.buscar_clientes_por_nombre(nombre, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar clientes por nombre: {str(e)}"
        )


@router.get("/tipo-persona/{tipo_persona}", response_model=List[ClienteResponse])
async def obtener_clientes_por_tipo_persona(
    tipo_persona: int,
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """
    Obtener clientes filtrados por tipo de persona
    
    - **tipo_persona**: 1=Persona Física, 2=Persona Moral
    - **skip**: Número de registros a saltar
    - **limit**: Número máximo de registros
    """
    try:
        if tipo_persona not in [1, 2]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El tipo de persona debe ser 1 (Física) o 2 (Moral)"
            )
        
        cliente_service = ClienteService(db)
        return cliente_service.obtener_clientes_por_tipo_persona(tipo_persona, skip=skip, limit=limit)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener clientes por tipo de persona: {str(e)}"
        )