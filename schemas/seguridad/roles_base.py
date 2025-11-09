from pydantic import BaseModel, Field
from typing import Optional


class RolesBase(BaseModel):
    """
    Schema base para Roles
    Contiene campos comunes que se comparten entre diferentes operaciones
    """
    rol: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Nombre del rol",
        example="Administrador"
    )
    
    descripcion: str = Field(
        ...,
        min_length=1,
        max_length=250,
        description="Descripción del rol",
        example="Rol con permisos completos del sistema"
    )
    
    estatus_id: int = Field(
        ...,
        gt=0,
        description="Estatus del rol (1=Activo, 0=Inactivo)",
        example=1
    )
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "rol": "Administrador",
                "descripcion": "Rol con permisos completos del sistema",
                "estatus_id": 1
            }
        }
