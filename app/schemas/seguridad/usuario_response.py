from pydantic import BaseModel, Field
from typing import Optional, List
from .usuario_rol_schemas import RolSimpleResponse
from datetime import datetime


class UsuarioResponse(BaseModel):
    """
    Schema para respuesta de usuario
    No incluye la contraseña por seguridad
    """
    id_usuario: int = Field(
        ...,
        description="ID único del usuario",
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
    
    estatus_id: int = Field(
        ...,
        description="Estatus del usuario (1=Activo, 0=Inactivo)",
        example=1
    )
    
    roles: List[RolSimpleResponse] = Field(
        default_factory=list,
        description="Lista de roles asignados al usuario"
    )
    
    class Config:
        from_attributes = True  # Para compatibilidad con SQLAlchemy
        json_schema_extra = {
            "example": {
                "id_usuario": 1,
                "login": "juan.perez",
                "correo_electronico": "juan.perez@gmail.com",
                "estatus_id": 1,
                "roles": [
                    {"id_rol": 1, "rol": "Administrador"},
                    {"id_rol": 2, "rol": "Usuario"}
                ]
            }
        }
