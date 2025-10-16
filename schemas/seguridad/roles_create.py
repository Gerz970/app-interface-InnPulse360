from pydantic import BaseModel, Field
from typing import Optional


class RolesCreate(BaseModel):
    """
    Schema para crear un nuevo rol
    Hereda de RolesBase pero sin id_rol
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
    
    estatus_id: Optional[int] = Field(
        1,  # Valor por defecto activo
        gt=0,
        description="Estatus del rol (1=Activo por defecto)",
        example=1
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "rol": "Administrador",
                "descripcion": "Rol con permisos completos del sistema",
                "estatus_id": 1
            }
        }
