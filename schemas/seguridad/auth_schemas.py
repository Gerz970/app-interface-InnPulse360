from pydantic import BaseModel, Field
from typing import Optional, List
from schemas.seguridad.usuario_rol_schemas import RolSimpleResponse


class UsuarioLogin(BaseModel):
    """
    Schema para login de usuario
    """
    login: str = Field(
        ...,
        min_length=1,
        max_length=25,
        description="Login del usuario",
        example="juan.perez"
    )
    
    password: str = Field(
        ...,
        min_length=1,
        description="Contraseña del usuario",
        example="123456"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "login": "juan.perez",
                "password": "123456"
            }
        }


class ModuloSimpleResponse(BaseModel):
    """
    Schema simplificado para módulo en respuesta de login
    """
    id_modulo: int = Field(
        ...,
        description="ID del módulo",
        example=1
    )
    
    nombre: str = Field(
        ...,
        description="Nombre del módulo",
        example="Dashboard"
    )
    
    descripcion: Optional[str] = Field(
        None,
        description="Descripción del módulo",
        example="Panel principal del sistema"
    )
    
    icono: Optional[str] = Field(
        None,
        description="Icono del módulo",
        example="fas fa-dashboard"
    )
    
    ruta: Optional[str] = Field(
        None,
        description="Ruta del módulo",
        example="/dashboard"
    )
    
    class Config:
        from_attributes = True


class PasswordTemporalInfo(BaseModel):
    """
    Schema para información de contraseña temporal
    """
    requiere_cambio: bool = Field(
        ...,
        description="Indica si el usuario debe cambiar su contraseña",
        example=True
    )
    
    password_expira: Optional[str] = Field(
        None,
        description="Fecha y hora de expiración de la contraseña temporal (ISO format)",
        example="2025-10-29T12:00:00"
    )
    
    dias_restantes: int = Field(
        ...,
        description="Días restantes antes de que expire la contraseña",
        example=5
    )
    
    mensaje: str = Field(
        ...,
        description="Mensaje informativo sobre la expiración",
        example="Debe cambiar su contraseña temporal. Expira en 5 días."
    )


class UsuarioInfo(BaseModel):
    """
    Schema para información básica del usuario
    """
    id_usuario: int = Field(
        ...,
        description="ID del usuario",
        example=1
    )
    
    login: str = Field(
        ...,
        description="Login del usuario",
        example="juan.perez"
    )
    
    correo_electronico: str = Field(
        ...,
        description="Correo electrónico del usuario",
        example="juan.perez@gmail.com"
    )
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    """
    Schema para respuesta de token JWT
    Estructura limpia sin redundancia
    """
    access_token: str = Field(
        ...,
        description="Token de acceso JWT",
        example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    )
    
    token_type: str = Field(
        default="bearer",
        description="Tipo de token",
        example="bearer"
    )
    
    expires_in: int = Field(
        ...,
        description="Tiempo de expiración del token en segundos",
        example=1800
    )
    
    usuario: UsuarioInfo = Field(
        ...,
        description="Información básica del usuario autenticado"
    )
    
    modulos: List[ModuloSimpleResponse] = Field(
        default_factory=list,
        description="Lista de módulos a los que el usuario tiene acceso"
    )
    
    roles: List[RolSimpleResponse] = Field(
        default_factory=list,
        description="Lista de roles del usuario con sus nombres"
    )
    
    password_temporal_info: Optional[PasswordTemporalInfo] = Field(
        None,
        description="Información sobre la contraseña temporal (solo si aplica)"
    )


class TokenData(BaseModel):
    """
    Schema para datos del token (payload)
    """
    id_usuario: Optional[int] = None
    login: Optional[str] = None
    correo_electronico: Optional[str] = None
