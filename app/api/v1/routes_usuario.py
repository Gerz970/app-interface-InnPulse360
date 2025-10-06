"""
Rutas API para gestión de usuarios
Incluye CRUD completo y autenticación
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from core.database_connection import get_database_session
from services.seguridad.usuario_service import UsuarioService
from schemas.seguridad.usuario_create import UsuarioCreate
from schemas.seguridad.usuario_update import UsuarioUpdate
from schemas.seguridad.usuario_response import UsuarioResponse
from schemas.seguridad.auth_schemas import UsuarioLogin, Token

# Configurar router
router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"],
    responses={404: {"description": "Not found"}},
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


# =============================================================================
# RUTAS DE AUTENTICACIÓN
# =============================================================================

@router.post("/login", response_model=Token, summary="Iniciar sesión")
async def login(
    login_data: UsuarioLogin,
    usuario_service: UsuarioService = Depends(get_usuario_service)
):
    """
    Iniciar sesión de usuario
    
    - **login**: Login del usuario
    - **password**: Contraseña del usuario
    
    Retorna un token JWT válido por 30 minutos.
    """
    return usuario_service.login(login_data)


# =============================================================================
# RUTAS CRUD DE USUARIOS
# =============================================================================

@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED, summary="Crear usuario")
async def create_usuario(
    usuario_data: UsuarioCreate,
    usuario_service: UsuarioService = Depends(get_usuario_service)
):
    """
    Crear un nuevo usuario
    
    - **login**: Login único del usuario (máximo 25 caracteres)
    - **correo_electronico**: Email único del usuario (máximo 50 caracteres)
    - **password**: Contraseña (mínimo 6 caracteres)
    - **estatus_id**: Estatus del usuario (1=Activo por defecto)
    
    La contraseña se encripta automáticamente antes de guardarse.
    """
    return usuario_service.create_usuario(usuario_data)


@router.get("/", response_model=List[UsuarioResponse], summary="Listar usuarios")
async def get_usuarios(
    skip: int = 0,
    limit: int = 100,
    current_user: UsuarioResponse = Depends(get_current_user),
    usuario_service: UsuarioService = Depends(get_usuario_service)
):
    """
    Obtener lista de usuarios activos con paginación
    
    - **skip**: Número de registros a saltar (default: 0)
    - **limit**: Número máximo de registros a retornar (default: 100)
    
    Requiere autenticación.
    """
    return usuario_service.get_all_usuarios(skip=skip, limit=limit)


@router.get("/{id_usuario}", response_model=UsuarioResponse, summary="Obtener usuario por ID")
async def get_usuario(
    id_usuario: int,
    current_user: UsuarioResponse = Depends(get_current_user),
    usuario_service: UsuarioService = Depends(get_usuario_service)
):
    """
    Obtener un usuario específico por su ID
    
    - **id_usuario**: ID del usuario a buscar
    
    Requiere autenticación.
    """
    usuario = usuario_service.get_usuario_by_id(id_usuario)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return usuario


@router.get("/login/{login}", response_model=UsuarioResponse, summary="Obtener usuario por login")
async def get_usuario_by_login(
    login: str,
    current_user: UsuarioResponse = Depends(get_current_user),
    usuario_service: UsuarioService = Depends(get_usuario_service)
):
    """
    Obtener un usuario específico por su login
    
    - **login**: Login del usuario a buscar
    
    Requiere autenticación.
    """
    usuario = usuario_service.get_usuario_by_login(login)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return usuario


@router.put("/{id_usuario}", response_model=UsuarioResponse, summary="Actualizar usuario")
async def update_usuario(
    id_usuario: int,
    usuario_data: UsuarioUpdate,
    current_user: UsuarioResponse = Depends(get_current_user),
    usuario_service: UsuarioService = Depends(get_usuario_service)
):
    """
    Actualizar un usuario existente
    
    - **id_usuario**: ID del usuario a actualizar
    - **login**: Nuevo login (opcional, debe ser único)
    - **correo_electronico**: Nuevo email (opcional, debe ser único)
    - **password**: Nueva contraseña (opcional, se encripta automáticamente)
    - **estatus_id**: Nuevo estatus (opcional)
    
    Todos los campos son opcionales. Solo se actualizan los campos proporcionados.
    Si se proporciona una nueva contraseña, se encripta automáticamente.
    
    Requiere autenticación.
    """
    usuario = usuario_service.update_usuario(id_usuario, usuario_data)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return usuario


@router.delete("/{id_usuario}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar usuario (lógico)")
async def delete_usuario(
    id_usuario: int,
    current_user: UsuarioResponse = Depends(get_current_user),
    usuario_service: UsuarioService = Depends(get_usuario_service)
):
    """
    Eliminar un usuario (eliminación lógica)
    
    - **id_usuario**: ID del usuario a eliminar
    
    Realiza una eliminación lógica cambiando el estatus a inactivo.
    El usuario no se elimina físicamente de la base de datos.
    
    Requiere autenticación.
    """
    success = usuario_service.delete_usuario(id_usuario)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )


# =============================================================================
# RUTAS ADICIONALES
# =============================================================================

@router.get("/me/profile", response_model=UsuarioResponse, summary="Obtener perfil actual")
async def get_my_profile(
    current_user: UsuarioResponse = Depends(get_current_user)
):
    """
    Obtener el perfil del usuario actualmente autenticado
    
    Retorna la información del usuario basada en el token JWT.
    """
    return current_user


@router.put("/me/profile", response_model=UsuarioResponse, summary="Actualizar perfil actual")
async def update_my_profile(
    usuario_data: UsuarioUpdate,
    current_user: UsuarioResponse = Depends(get_current_user),
    usuario_service: UsuarioService = Depends(get_usuario_service)
):
    """
    Actualizar el perfil del usuario actualmente autenticado
    
    - **login**: Nuevo login (opcional, debe ser único)
    - **correo_electronico**: Nuevo email (opcional, debe ser único)
    - **password**: Nueva contraseña (opcional, se encripta automáticamente)
    - **estatus_id**: Nuevo estatus (opcional)
    
    Actualiza el perfil del usuario basado en el token JWT.
    """
    usuario = usuario_service.update_usuario(current_user.id_usuario, usuario_data)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return usuario
