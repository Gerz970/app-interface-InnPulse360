"""
Rutas API para gestión de tokens de dispositivos y notificaciones push
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from core.database_connection import get_database_session
from services.seguridad.usuario_service import UsuarioService
from schemas.seguridad.usuario_response import UsuarioResponse
from schemas.notifications.device_token_schemas import DeviceTokenRequest, DeviceTokenResponse
from dao.seguridad.dao_device_token import DeviceTokenDAO

# Configurar router
router = APIRouter(
    prefix="/notifications",
    tags=["notifications"],
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


@router.post("/register-token", response_model=DeviceTokenResponse, summary="Registrar token de dispositivo")
async def register_device_token(
    request: DeviceTokenRequest,
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """
    Registrar token de dispositivo para recibir notificaciones push
    
    Se llama automáticamente después del login o cuando el token FCM se renueva.
    Solo el usuario autenticado puede registrar su propio token.
    Los tokens se guardan en la base de datos.
    
    - **device_token**: Token FCM del dispositivo
    - **plataforma**: Plataforma del dispositivo ('android' o 'ios')
    """
    try:
        device_token_dao = DeviceTokenDAO(db)
        device_token_dao.create_or_update(
            usuario_id=current_user.id_usuario,
            device_token=request.device_token,
            plataforma=request.plataforma
        )
        return DeviceTokenResponse(
            success=True,
            message="Token registrado exitosamente en la base de datos"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al registrar token: {str(e)}"
        )


@router.post("/unregister-token", response_model=DeviceTokenResponse, summary="Desregistrar tokens de dispositivo")
async def unregister_device_token(
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """
    Desregistrar tokens de dispositivo (útil para logout)
    
    Marca todos los tokens del usuario como inactivos en la base de datos.
    Esto evita que se envíen notificaciones a dispositivos donde el usuario
    ya cerró sesión.
    """
    try:
        device_token_dao = DeviceTokenDAO(db)
        tokens_desactivados = device_token_dao.deactivate_by_usuario_id(current_user.id_usuario)
        
        if tokens_desactivados:
            return DeviceTokenResponse(
                success=True,
                message="Tokens desregistrados exitosamente"
            )
        else:
            return DeviceTokenResponse(
                success=True,
                message="No había tokens activos para desregistrar"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al desregistrar tokens: {str(e)}"
        )

