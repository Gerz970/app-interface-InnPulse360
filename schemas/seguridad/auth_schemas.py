from pydantic import BaseModel, Field
from typing import Optional


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


class Token(BaseModel):
    """
    Schema para respuesta de token JWT
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
        example=3600
    )
    
    user_info: dict = Field(
        ...,
        description="Información básica del usuario",
        example={
            "id_usuario": 1,
            "login": "juan.perez",
            "correo_electronico": "juan.perez@gmail.com"
        }
    )


class TokenData(BaseModel):
    """
    Schema para datos del token (payload)
    """
    id_usuario: Optional[int] = None
    login: Optional[str] = None
    correo_electronico: Optional[str] = None
