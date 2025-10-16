from pydantic import BaseModel, Field
from typing import Optional


class RolesResponse(BaseModel):
    """
    Schema para respuestas de Roles
    Incluye el ID del rol y excluye información sensible
    """
    id_rol: int = Field(
        ...,
        description="ID único del rol",
        example=1
    )
    
    rol: str = Field(
        ...,
        description="Nombre del rol",
        example="Administrador"
    )
    
    descripcion: str = Field(
        ...,
        description="Descripción del rol",
        example="Rol con permisos completos del sistema"
    )
    
    estatus_id: int = Field(
        ...,
        description="Estatus del rol",
        example=1
    )
    
    class Config:
        from_attributes = True  # Para compatibilidad con SQLAlchemy
        json_schema_extra = {
            "example": {
                "id_rol": 1,
                "rol": "Administrador",
                "descripcion": "Rol con permisos completos del sistema",
                "estatus_id": 1
            }
        }
