from pydantic import BaseModel, Field
from typing import List, Optional


class UsuarioRolAssign(BaseModel):
    """
    Schema para asignar un rol a un usuario
    """
    usuario_id: int = Field(
        ...,
        description="ID del usuario",
        example=1
    )
    
    rol_id: int = Field(
        ...,
        description="ID del rol a asignar",
        example=1
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "usuario_id": 1,
                "rol_id": 1
            }
        }


class UsuarioRolBulkAssign(BaseModel):
    """
    Schema para asignación masiva de roles a un usuario
    """
    roles_ids: List[int] = Field(
        ...,
        description="Lista de IDs de roles a asignar",
        example=[1, 2, 3]
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "roles_ids": [1, 2, 3]
            }
        }


class RolSimpleResponse(BaseModel):
    """
    Schema simplificado para mostrar rol en respuestas de usuario
    """
    id_rol: int = Field(
        ...,
        description="ID del rol",
        example=1
    )
    
    rol: str = Field(
        ...,
        description="Nombre del rol",
        example="Administrador"
    )
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id_rol": 1,
                "rol": "Administrador"
            }
        }
